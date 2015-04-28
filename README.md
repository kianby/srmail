## Simple RESTful Mailer

Small piece of code providing a simple way to send and receive emails via a RESTful API. Because of security considerations, SRMail is likely to listen on localhost and provide e-mail services to other applications running on the same host. SRMail is written in Python 3.

### API by example

**Read inbox message count**

GET /mbox => count as JSON

    curl http://localhost:8000/mbox 
    => {"count": 3}

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
Attachments are stored in a separate attribute 'attachment'.

**Delete a message**

DELETE /mbox/\<index\> => 200 or 500

**Send a message**

POST /mbox => 200 or 500

    curl -X POST -H "Content-Type: application/json; charset=utf-8" 
         -d '{"to":"bill@phoenix.com", "subject":"Got it", "content":"See you soon!\n\n-- John"}'      
         http://localhost:8000/mbox
    => 200
    
