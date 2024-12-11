import requests
import pandas as pd
from tqdm.notebook import tqdm
from fuzzywuzzy import fuzz 
from nicknames import NickNamer
from collections import defaultdict
import time
from .search_py import SearchType

def institution_id_openalex(university_name):
    """
    input: 
         uni_name: the name of the university or institution
    output:
         university_id: the openalex id of the university
    """
 
    # search an university based on its name; and only return the id, the display_name and works_count in the database
    url=f'https://api.openalex.org/institutions?search={university_name}&select=id,display_name,works_count'
        
    response = requests.get(url)
    
    if response.status_code!=200:
        print('The webpage cannot be fetched!')
        
    data = response.json()
    count=data['meta']['count']
    
    
    # check the number of items returned
    if count==0:
        print('no match for the institution!')
        
    elif count==1:
        university_id=data['results'][0]['id']
        
    else:
        # Find the ID of the university with the most publications   
        university_with_max = max(data['results'], key=lambda x: x["works_count"])
        university_id = university_with_max["id"]
        
    university_id=university_id.split('/')[-1]

    return university_id

def nameParser(person_name):
     
     """
    Input
      person_name: the name of a person
      
    Output
      first_name: person's first name
      last_name: person's last name
      
    """
     name_split = person_name.strip().split()
     if (len(name_split) < 2):
          return "Invalid Name, need both first and last"
     first_name = name_split[0]
     last_name = name_split[-1]
    
     return first_name, last_name

def list_person_ids_openalex(person_name, university_id):
    """
    Input
      person_name: the name of a person
      university_id: openalex university ID
    Output
      person_ids: a list of openalex ids matched
    """
    nn = NickNamer()
    first, last = nameParser(person_name)
    totalNames = {first} | set(nn.nicknames_of(first)) | set(nn.canonicals_of(first))
    typeOfSearchConducted = SearchType.EXACT_NAME
    
    ids = []
    bestNameMatch = first
    
    def search_with_name(name):
        url = f'https://api.openalex.org/authors?filter=affiliations.institution.id:{university_id}&search={name}%20{last}'
        trycnt = 3
        while trycnt > 0:
            try:
                response = requests.get(url)
                if response.status_code != 200:
                    print(f'The webpage cannot be fetched for {name} {last}!')
                    break
                
                data = response.json()
                
                idUrl = [result['id'] for result in data['results']]
                return [url.split('/')[-1] for url in idUrl]
                
            except (ConnectionError, ConnectionResetError) as ex:
                if trycnt <= 1:
                    print(f"Failed to retrieve: {url}\n{str(ex)}")  # Done retrying
                else:
                    print(f"Retrying... ({3 - trycnt + 1}/3)")
                    trycnt -= 1  # Decrement retry counter
                    time.sleep(0.5)  # Wait half a second before retrying
        return []

    ids.extend(search_with_name(first))

    # First, search with all names in totalNames
    if not ids:
        for firstName in totalNames:
            ids.extend(search_with_name(firstName))
            #If the nickname search returns results, update the first name to the best matching name. 
            if ids:
                bestNameMatch = firstName
                break
        person_name = f"{bestNameMatch} {last}"

    # If no results found, search with initial
    if not ids:
        #Try searching with first middle initial
        if len(first) == 2:
            initials = first[0] + ".%20" + first[1] + "."
            ids.extend(search_with_name(initials))
            typeOfSearchConducted = SearchType.FIRST_MIDDLE_INITIAL
        #Try searching with first initial
        else:
            initial = first[0] + "."
            ids.extend(search_with_name(initial))
            typeOfSearchConducted = SearchType.FIRST_INITIAL
    return ids, typeOfSearchConducted, person_name

def choose_person(person_ids, person_name, university_id, typeOfSearchConducted):
    '''
    
    Input
      person_name: the name of a person
      person_ids: assoicated ids with a person (can be found with list_persons_ids_openalex)
      university_id: university id 
      typeOfSearchConducted: enumerated type representing type of name search conducted
      
    Output
      selectID: best openalex id match for author name


    '''
    filtered_persons_ids = []
    selectID = " "
    maxCiteCount = -1
    firstName, lastName = nameParser(person_name)
    maxNameSimilarity = 0
    highThres, lowThres = 76, 65

    #Iterate through list of ids
    for id in person_ids:
        url = f'https://api.openalex.org/people/{id}'
        trycnt = 3
        
        while trycnt > 0:
            try:
                response = requests.get(url)
                if response.status_code != 200:
                    print(f'The webpage cannot be fetched for {person_name}!')
                    break
                
                data = response.json()
                affiliations = data.get('affiliations', [])
                institution_ids = [aff['institution']['id'].split('/')[-1] for aff in affiliations]

                # Proceed only if the specified university_id is in the list of institution_ids
                if university_id not in institution_ids:
                    break
                
                filtered_persons_ids.append(id)

                #Calculating fuzz ratio between the input name and the API name of id.
                apiFirstName, apiLastName = nameParser(data['display_name'])
                apiDisplayName = apiFirstName + " " + apiLastName
                name_similarity = fuzz.ratio(person_name, apiDisplayName)

                #Change fuzz string matching threshold based on search type
                if (typeOfSearchConducted == SearchType.FIRST_INITIAL):
                    threshold = highThres
                elif (typeOfSearchConducted == SearchType.EXACT_NAME):
                    threshold = lowThres
                else:
                    threshold = 0
                
                #Filtering name based on fuzz score 
                if name_similarity >= threshold:
                    if (typeOfSearchConducted == SearchType.FIRST_INITIAL or typeOfSearchConducted == SearchType.FIRST_MIDDLE_INITIAL):
                        if (firstName[0].lower() != apiFirstName[0].lower()):
                            print(f"{id} has initial mismatch: not a valid name")
                            break
                    if name_similarity > maxNameSimilarity:
                        maxNameSimilarity = name_similarity
                        maxCiteCount = data['cited_by_count']
                        selectID = id
                    #If scores are equal, sort by author with most citations
                    elif name_similarity == maxNameSimilarity:
                        if data['cited_by_count'] > maxCiteCount:
                            maxCiteCount = data['cited_by_count']
                            selectID = id
                else:
                    print(f'{id} has not met string matching threshold: not a valid name')
    
                trycnt = 0  # Success, exit retry loop

            except (ConnectionResetError, ConnectionError) as ex:
                if trycnt <= 1:
                    print(f"Failed to retrieve: {url}\n{str(ex)}")  
                else:
                    print(f"Retrying... ({3 - trycnt + 1}/3)")
                    trycnt -= 1 
                    time.sleep(0.5)  

    return selectID
   