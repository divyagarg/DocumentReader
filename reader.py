import urllib2

from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.cf313744-8d37-4ffd-9d8b-9294979bbd45"):
        raise ValueError("Invalid Application ID")

    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        print('On Launch')
        return on_launch(event["request"], event["session"])

    elif event["request"]["type"] == "IntentRequest":
        print('On Intent')
        return on_intent(event["request"], event["session"])

    elif event["request"]["type"] == "SessionEndedRequest":
        return handle_session_end_request


def on_session_started(session_started_request, session):
    print("Starting new session.")


def on_launch(launch_request, session):
    return get_welcome_response()


def get_welcome_response():
    session_attributes = {}
    card_title = "DOCUMENT READER"
    speech_output = "Welcome to the Alexa Document Reader skill. " \
                    "You can ask me for read a hardcoded document."
    reprompt_text = "Please ask me to read out document"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }


def get_hardcoded_text():
    session_attributes = {}
    speech_output = "Once there was a king."
    res = build_speechlet_response(title="Document Reader",
                                   output=speech_output,
                                   reprompt_text='',
                                   should_end_session=False)
    return build_response(session_attributes, res)


def get_pdf_data():
    session_attributes = {}
    response = urllib2.urlopen("http://che.org.il/wp-content/uploads/2016/12/pdf-sample.pdf")
    with open('/tmp/pdf-sample.pdf', 'wb') as f:
        f.write(response.read())
    speech_output = convert('/tmp/pdf-sample.pdf')
    res = build_speechlet_response(title="Document Reader",
                                   output=speech_output,
                                   reprompt_text='',
                                   should_end_session=False)
    return build_response(session_attributes, res)


def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text



def on_intent(intent_request, session):
    intent_name = intent_request["intent"]["name"]
    if intent_name == "ReadHardCodedDoc":
        return get_pdf_data()
    else:
        raise ValueError("Invalid intent")


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }



def handle_session_end_request():
    card_title = "DOCUMENT READER - Thanks"
    speech_output = "Thank you for using the DOCUMENT READER skill.  See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))



event = {
  "session": {
    "new": False,
    "sessionId": "SessionId.3b60649c-ace8-47d6-827a-029b7bf72b3c",
    "application": {
      "applicationId": "amzn1.ask.skill.cf313744-8d37-4ffd-9d8b-9294979bbd45"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.AEKA6TCTTTEGKAIGLK274CO6DEBZ7MMHUVIIWNXVYHGL5TCVUMH43KEBVTU7TQD2IRRFPGVUTKCQ5W36HETD3V4YSRNKCWIRC62TWEWGRT3W7J3R5RDBCXIYNJSE5PCMXIXAOTOBCRXPGARCF6PCCQJR3ZCWEIHGSCQGLO3PX4FQEI4IPPTSR66USVWIOQHJB4EBNR6YQKZLAKI"
    }
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.9b35212f-9ab2-4932-b4fb-ff00a5a2f671",
    "intent": {
      "name": "ReadHardCodedDoc",
      "slots": {}
    },
    "locale": "en-US",
    "timestamp": "2017-08-21T09:35:26Z"
  },
  "context": {
    "AudioPlayer": {
      "playerActivity": "IDLE"
    },
    "System": {
      "application": {
        "applicationId": "amzn1.ask.skill.cf313744-8d37-4ffd-9d8b-9294979bbd45"
      },
      "user": {
        "userId": "amzn1.ask.account.AEKA6TCTTTEGKAIGLK274CO6DEBZ7MMHUVIIWNXVYHGL5TCVUMH43KEBVTU7TQD2IRRFPGVUTKCQ5W36HETD3V4YSRNKCWIRC62TWEWGRT3W7J3R5RDBCXIYNJSE5PCMXIXAOTOBCRXPGARCF6PCCQJR3ZCWEIHGSCQGLO3PX4FQEI4IPPTSR66USVWIOQHJB4EBNR6YQKZLAKI"
      },
      "device": {
        "supportedInterfaces": {}
      }
    }
  },
  "version": "1.0"
}
lambda_handler(event, None)