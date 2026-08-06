## Adding a Copy Button Without a Code Block
> 
> 
> `This will copy the following text: <copy>Text to copy</copy>`   
> 
> This will copy the following text: <copy>Text to copy</copy>

## Adding user specific variables into your lab guide
> There may be times in which you want to embed some attendee specific information into the instructions of your lab guide, like credentials or phone numbers, which will be used on multiple pages of your lab guide.  You can gather the information via a form or you can pass a pre-encoded JSON string as a URL parameter to populate the variable values into the browser's session storage.  Then you can use a simple HTML tag with a special class name to update the values in the lab guide. 
> This feature can be combined with the copy button method above.

### Form Method
??? "Show me the code"
    ```html
    <form id="info">


    <label for="Admin">Admin Login:</label>
    <input type="text" id="Admin" name="Admin"><br>
    
    <label for="PW">Admin Password:</label>
    <input type="text" id="PW" name="PW"><br>
    
    <label for="EP">Inbound Channel Name:</label>
    <input type="text" id="EP" name="EP"><br>

    <label for="DN">Inbound Channel Phone Number:</label>
    <input type="text" id="DN" name="DN"><br>

    <label for="Queue">Queue 1 Name:</label>
    <input type="text" id="Queue" name="Queue"><br>
    
    <label for="Queue2">Queue 2 Name:</label>
    <input type="text" id="Queue2" name="Queue2"><br>

    <label for="Team">Team 1 Name:</label>
    <input type="text" id="Team" name="Team"><br>

    <label for="Team2">Team 2 Name:</label>
    <input type="text" id="Team2" name="Team2"><br>
    <br>
    <button onclick="setValues()">Update Lab Guide</button>
    </form>

    > Login: <copy><w class="Admin">Provided by proctor</w></copy>
    > 
    > Password: <copy><w class="PW">Provided by proctor</w></copy>
    >
    > Assigned Inbound Channel Name: <copy><w class="EP">Provided by proctor</w></copy>
    > 
    > Assigned Inbound Channel Number: <copy><w class="DN">Provided by proctor</w></copy>
    >
    > Assigned Queue Name 1: <copy><w class="Queue">Provided by proctor</w></copy>
    >
    > Assigned Queue Name 2: <copy><w class="Queue2">Provided by proctor</w></copy>
    >
    > Assigned Team name 1: <copy><w class="Team">Provided by proctor</w></copy>
    >
    > Assigned Team name 2: <copy><w class="Team2">Provided by proctor</w></copy>
    ```
 
<div class="grid" markdown>

<form id="info">
<label for="info">Example Input Form</label><br>

  <label for="Admin">Admin Login:</label>
  <input type="text" id="Admin" name="Admin"><br>
  
  <label for="PW">Admin Password:</label>
  <input type="text" id="PW" name="PW"><br>
  
  <label for="EP">Inbound Channel Name:</label>
  <input type="text" id="EP" name="EP"><br>

  <label for="DN">Inbound Channel Phone Number:</label>
  <input type="text" id="DN" name="DN"><br>

  <label for="Queue">Queue 1 Name:</label>
  <input type="text" id="Queue" name="Queue"><br>
  
  <label for="Queue2">Queue 2 Name:</label>
  <input type="text" id="Queue2" name="Queue2"><br>

  <label for="Team">Team 1 Name:</label>
  <input type="text" id="Team" name="Team"><br>

  <label for="Team2">Team 2 Name:</label>
  <input type="text" id="Team2" name="Team2"><br>
  <br>
  <button onclick="setValues()">Update Lab Guide</button>
</form>

> Login: <copy><w class="Admin">Provided by proctor</w></copy>
> 
> Password: <copy><w class="PW">Provided by proctor</w></copy>
>
> Assigned Inbound Channel Name: <copy><w class="EP">Provided by proctor</w></copy>
> 
> Assigned Inbound Channel Number: <copy><w class="DN">Provided by proctor</w></copy>
>
> Assigned Queue Name 1: <copy><w class="Queue">Provided by proctor</w></copy>
>
> Assigned Queue Name 2: <copy><w class="Queue2">Provided by proctor</w></copy>
>
> Assigned Team name 1: <copy><w class="Team">Provided by proctor</w></copy>
>
> Assigned Team name 2: <copy><w class="Team2">Provided by proctor</w></copy>
</div>
---

### URL Method
> If you have a lot of attendee variables in your lab, you may choose to precompile and encode them so that you can simply provide a URL link which will load all of their required information.
> 
> To see this in action, add this string at the end of the URL for any page on this site: <copy>?eyJBZG1pbiI6ImFkbWluQHh5ei5iaXoiLCJQVyI6InNVcGVyU2VjcmV0MTIzISIsIkVQIjoiRVAxIiwiRE4iOiIrMTkxMDU1NTEyMTUyIiwiUXVldWUiOiJRdWV1ZTEiLCJRdWV1ZTIiOiJRdWV1ZTIiLCJUZWFtIjoiVGVhbTEiLCJUZWFtMiI6IlRlYW0yIn0=</copy>