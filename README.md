# Bio-Web-Application
Uol Advanced Web Development CM3035 Midterm

This is a RESTFUL API application done with Python and Django, that contains gene data from the csv file, to allow researchers to query data from the database as and when they need. 
A detailed explanation can be found at "midterm report.pdf". "rest_specification_and_examples.txt" shows examples of gene data retrieved from the API

### How to run the application:
1) Navigate to virtual environment: cd midterm_venv/bin
2) Activate virtual environment: source activate
3) Navigate to source code: cd bioweb
4) Populate database with csv file: python3 ./scripts/populate_db.py     [Loading CSV takes about 30 seconds...]
5) Run server: python3 manage.py runserver
6) Base url to access API: http://127.0.0.1:8000/api/

### Refer to this url list:
<kbd><img src="https://user-images.githubusercontent.com/62084317/226915788-a155c1ed-0235-4ff9-a530-f29bfaa9a59d.png" width="800"></kbd>
<br><br><br>



### Examples:
<kbd>
  http://127.0.0.1:8000/api/protein/A0A016S8J7  -  returns the protein sequence data
  <img src="https://user-images.githubusercontent.com/62084317/226919100-274b3d20-47a1-41d7-bf1d-9bd5a9a14806.png" width="500">
  
  
  http://127.0.0.1:8000/api/pfam/PF00360  -  return the domain and it's description
  <img src="https://user-images.githubusercontent.com/62084317/226919120-26e1924e-b9fd-49f6-b300-8b5d5303b325.png" width="500">
  
  http://127.0.0.1:8000/api/pfams/55661  -  return a list of all domains in all the proteins for a given organism
  <img src="https://user-images.githubusercontent.com/62084317/226918767-6ae98ab4-ba89-4a7c-a780-bf9056acbb35.png" width="500">
</kbd>
<br><br><br>
