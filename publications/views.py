from django.views.generic import ListView
from django.shortcuts import render
import requests
from xml.etree import ElementTree as ET

class PublicationListView(ListView):
    template_name = 'publications/publication_list.html'
    context_object_name = 'publications'

    def get_queryset(self):
        first_name = self.kwargs.get('first_name', 'Yansong')
        last_name = self.kwargs.get('last_name', 'Miao')
        full_name = f"{first_name} {last_name}"  # Format: "LastName FirstName"

        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

        # Step 1: Search for the author's publications
        search_params = {
            "db": "pubmed",
            "term": full_name + "[Author]",
            "retmax": "100",  # Max number of results to fetch
            "retmode": "json"
        }
        search_response = requests.get(search_url, params=search_params)
        search_data = search_response.json()
        id_list = search_data.get("esearchresult", {}).get("idlist", [])

        publications = []

        if id_list:
            # Step 2: Fetch details for each publication
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(id_list),
                "retmode": "xml"
            }
            fetch_response = requests.get(fetch_url, params=fetch_params)
            fetch_data = fetch_response.content

            # Parse the XML response
            root = ET.fromstring(fetch_data)
            for article in root.findall(".//PubmedArticle"):
                title = article.findtext(".//ArticleTitle")
                journal = article.findtext(".//Journal/Title")
                year = article.findtext(".//PubDate/Year")
                volume = article.findtext(".//JournalIssue/Volume")
                issue = article.findtext(".//JournalIssue/Issue")
                pages = article.findtext(".//Pagination/MedlinePgn")

                # Extract DOI
                doi = None
                for elocation_id in article.findall(".//ELocationID"):
                    if elocation_id.get("EIdType") == "doi":
                        doi = elocation_id.text
                        break
                
                authors_list = []
                for author in article.findall(".//Author"):
                    last_name = author.findtext(".//LastName")
                    initials = author.findtext(".//Initials")
                    if last_name and initials:
                        authors_list.append(f"{last_name} {initials}")
                    elif last_name:
                        authors_list.append(last_name)
                    elif initials:
                        authors_list.append(initials)

                publications.append({
                    'title': title,
                    'authors': authors_list,
                    'journal': journal,
                    'year': year,
                    'volume': volume,
                    'issue': issue,
                    'pages': pages,
                    'doi': doi,
                })
                
        return publications

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_author'] = self.kwargs.get('name_used_for_publication', 'Miao Y')  # Pass the target author name to the context
        return context