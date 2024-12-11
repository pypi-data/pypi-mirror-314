import requests
from nicknames import NickNamer
from .person_match import nameParser
import time


#Returns topic id based on topic name
def topic_id_openAlex(topicName):

    if not topicName.replace(" ", "").isalpha():
        raise ValueError("topic name can only include alphabetic characters")
    
    url = f"https://api.openalex.org/topics?search={topicName}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f'The webpage cannot be fetched for {topicName}!')

    data = response.json()
    if data['meta']['count'] == 0:
        return f"{topicName} is an invalid topic name"
    else:
        topicID = data['results'][0]['id']
        topicID = topicID.split("/")[-1]
    return topicID


def list_person_ids_openalex_by_topic(person_name, university_id, topicID):
    """
    Input
      person_name: the name of a person
      university_id: openalex university id
      topicID: openalex topic id
      
    Output
      person_ids: a list of openalex ids matched based on filters
    """
    nn = NickNamer()
    first, last = nameParser(person_name)
    totalNames = {first} | set(nn.nicknames_of(first)) | set(nn.canonicals_of(first))
    ids = []
    
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
                
                filtered_ids = []
                for result in data['results']:
                    author_concepts = [concept['id'].split('/')[-1] for concept in result.get('topics', [])]
                    if topicID in author_concepts:
                        filtered_ids.append(result['id'].split('/')[-1])  
                
                return filtered_ids
                
            except (ConnectionError, ConnectionResetError) as ex:
                if trycnt <= 1:
                    print(f"Failed to retrieve: {url}\n{str(ex)}")  
                else:
                    print(f"Retrying... ({3 - trycnt + 1}/3)")
                    trycnt -= 1  
                    time.sleep(0.5)  

    # First, search with all names in totalNames
    for firstName in totalNames:
        ids.extend(search_with_name(firstName))
    
    # If no results found, search with initial
    if not ids:
        if len(first) == 2:
            initials = first[0] + ".%20" + first[1] + "."
            ids.extend(search_with_name(initials))
        else:
            initial = first[0] + "."
            ids.extend(search_with_name(initial))
    return ids

#Returns openalex id based on orcid id
def search_orcid_ID(id):

     url = f'https://api.openalex.org/authors?filter=orcid:{id}'
     response = requests.get(url)
     data = response.json()
      
     if not data.get('results'):
        print("No author found for orcid id")
        return None

     openalex_id = data['results'][0]['ids']["openalex"]
     if not openalex_id:
        print("OpenAlex ID not found in the response.")
        return None
     
     openalex_id = openalex_id.split("/")[-1]

     return openalex_id

     