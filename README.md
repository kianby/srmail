## Simple RESTful Mailer

Small piece of code providing a simple way to send and receive emails via a
RESTful API. Because of security considerations, SRMail is likely to listen on
localhost and provide e-mail services to other applications running on the same
host. For that purpose SRMail manages an email account via IMAP and SMTP.

Requirements: 

- Python 3.7
- pip libs: flask flask-apscheduler peewee clize profig 

### Configuration

Configuration is a .ini file.

    ; Default configuration
    [main]
    db_url = sqlite:///db.sqlite

    [imap]
    polling = 120
    host = mail.gandi.net
    ssl = false
    port = 143
    login = blog@mydomain.com
    password = MYPASSWORD

    [smtp]
    host = mail.gandi.net
    starttls = true
    port = 587
    login = blog@mydomain.com
    password = MYPASSWORD

    [http]
    host = 127.0.0.1
    port = 8000

### API by example

**Read inbox message count**

GET /mbox => count as JSON

    curl http://localhost:8000/mbox
    => {
          "count": 1,
          "emails": [
              {
                  "datetime": "2018-09-09 17:21:02",
                  "encoding": "UTF-8",
                  "from": "Yanx <yax@mydomain.com>",
                  "subject": "Test"
              }
          ]
        }

**Read a message**

GET /mbox/\<index\> => message as JSON

    curl http://localhost:8000/mbox/1
    =>
    {
      "datetime": "2015-04-26 20:21:38",
      "encoding": "UTF-8",
      "from": "Bill <bill@phoenix.com>",
      "index": 1,
      "parts": [
        {
            "content": "Some plain text here. \r\n\r\nBye",
            "content-type": "text/plain"
        },
      ]
      "subject": "Test",
      "to": "john@phoenix.com"
    }

Parts are text/plain or text/html.
Attachments are stored in a separate attribute named 'attachments'.

**Delete a message**

DELETE /mbox/\<index\> => 200 (Ok) or 500 (Internal Server Error)

Be careful if you intend to delete several messages. Deleting a message
renumbers other inbox messages.

**Send a message**

POST /mbox => 200 (Ok) or 500 (Internal Server Error)

    curl -X POST -H "Content-Type: application/json; charset=utf-8"
         -d '{"to":"bill@phoenix.com", "subject":"Got it",
              "content":"See you soon!\n\n-- John"}'
         http://localhost:8000/mbox
    => 200

A plain-text email is sent.
