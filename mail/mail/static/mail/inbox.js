document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email)

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector("#email_details_view").style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function send_email(event){
  //Modifies the default beheavor so it doesn't reload the page after submitting.

  event.preventDefault();
  console.log("test")
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector("#compose-recipients").value,
        subject: document.querySelector("#compose-subject").value,
        body: document.querySelector("#compose-body").value,
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox("sent")
  });
}



function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector("#email_details_view").style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);
    emails.forEach((email) => {
      const element = document.createElement('div');
      element.innerHTML = `<p>${email.sender}</p> <h5>${email.subject}</h5> <p>${email.timestamp}</p>`
      element.className = 'DivContent list-group-item'
      if (email.read === false){
        element.style.backgroundColor = "white"
      }
      else{
        element.style.backgroundColor = "lightgrey"
      }
      element.addEventListener('click', function() {
        fetch(`/emails/${email.id}`)
        .then(response => response.json())
        .then(email_details => {
            
          document.querySelector('#emails-view').style.display = 'none';
          document.querySelector('#compose-view').style.display = 'none';
          document.querySelector("#email_details_view").style.display = 'block';

          document.querySelector("#email_details_view").innerHTML = `
              <p>From: ${email_details.sender}</p> 
              <p>To: ${email_details.recipients}</p> 
              <p>Subject: ${email_details.subject}</p> 
              <p>Date: ${email_details.timestamp}</p> 
              <p>${email_details.body}</p>    
        `
        const reply_button = document.createElement('button');
        reply_button.innerHTML = "Reply"
        reply_button.className = "btn btn-success mx-1" 
        reply_button.addEventListener("click", ()=>{
            
            document.querySelector('#emails-view').style.display = 'none';
            document.querySelector('#compose-view').style.display = 'block';
            document.querySelector("#email_details_view").style.display = 'none';

            let subject = email_details.subject;
            //console.log(subject.split(" ", 1)[0]);
            if (subject.split(" ", 1)[0] != "Re:") {
              subject = "Re: " + subject;
            }
            document.querySelector('#compose-recipients').value = email_details.sender;
            document.querySelector('#compose-subject').value = subject;
            document.querySelector('#compose-body').value = `On ${email_details.timestamp} ${email_details.sender} wrote: ${email_details.body}`;
            
        })
        document.querySelector('#email_details_view').append(reply_button);


          if (mailbox !== "sent"){

          
          
          const archive_button = document.createElement('button');
          if (email_details.archived === false){
              archive_button.innerHTML = "Archive"
              archive_button.className = "btn btn-danger"
              archive_button.addEventListener("click", ()=>{
                fetch(`/emails/${email.id}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                      archived: true
                  })
                })
                .then(response => load_mailbox("inbox"))
              })
          }

          else{
              archive_button.innerHTML = "Unarchive"
              archive_button.className = "btn btn-warning"
              archive_button.addEventListener("click", ()=>{
                fetch(`/emails/${email.id}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                      archived: false
                  })
                })
                .then(response => load_mailbox("inbox"))
              })

          }          

          document.querySelector('#email_details_view').append(archive_button);
          //element.innerHTML = 

          }


          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          })
            
        });
      });
      document.querySelector('#emails-view').append(element);
      console.log(email)
    })

    // ... do something else with emails ...
  });

}