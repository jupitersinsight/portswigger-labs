### Lab: Web shell upload via race condition

This lab contains a vulnerable image upload function.
Although it performs robust validation on any files that are uploaded, it is possible to bypass this validation entirely by exploiting a race condition in the way it processes them.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file /home/carlos/secret. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter


_____

**HINT**

The vulnerable code that introduces this race condition is as follows:

<?php
$target_dir = "avatars/";
$target_file = $target_dir . $_FILES["avatar"]["name"];

// temporary move
move_uploaded_file($_FILES["avatar"]["tmp_name"], $target_file);

if (checkViruses($target_file) && checkFileType($target_file)) {
    echo "The file ". htmlspecialchars( $target_file). " has been uploaded.";
} else {
    unlink($target_file);
    echo "Sorry, there was an error uploading your file.";
    http_response_code(403);
}

function checkViruses($fileName) {
    // checking for viruses
    ...
}

function checkFileType($fileName) {
    $imageFileType = strtolower(pathinfo($fileName,PATHINFO_EXTENSION));
    if($imageFileType != "jpg" && $imageFileType != "png") {
        echo "Sorry, only JPG & PNG files are allowed\n";
        return false;
    } else {
        return true;
    }
}
?>



_____

Exploit:
Since the uploaded file is store in a public folder (/files/avatars/filename.extension) for a few millieseconds while it is being checked, it is possibile to send a lot of requests for that file and have it executed before it is deleted.
1) Upload the php shell
2) Call for the file before it is removed

In Burp:
1) Fake Intruder attack with GET request for the file
2) While intruder is running, send a POST request via Repeater
3) Stop Intruder attack and look for request with status code 200


_____

Script:
Multithreaded HTTP Requests to send multiple requests in a short window of time



