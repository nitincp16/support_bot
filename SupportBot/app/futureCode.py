
# Helper function to parse message for Slack replies
def parse_message(text):
    data = {}
    if "issue :" in text.lower() and "reason :" in text.lower() and "solution :" in text.lower():
        parts = text.lower().split(",")
        for part in parts:
            if "issue :" in part:
                data['issue'] = part.split("issue :")[1].strip()
            if "reason :" in part:
                data['reason'] = part.split("reason :")[1].strip()
            if "solution :" in part:
                data['solution'] = part.split("solution :")[1].strip()
    return data

# Endpoint to receive Slack events
@app.post("/slack/events")
async def slack_events(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    event = payload.get("event", {})
    event_type = event.get("type")

    if "challenge" in payload:
        return {"challenge": payload["challenge"]}

    if event_type == "message":
        user_id = event.get("user")
        text = event.get("text")
        channel_id = event.get("channel")

        data = parse_message(text)
        if 'issue' in data and 'reason' in data and 'solution' in data:
            issue = data['issue']
            reason = data['reason']
            solution = data['solution']

            # Update the issue in the Supabase database
            response = supabase.table('issues').update({
                'reason': reason,
                'solution': solution,
                'encoded_data': json.dumps({"issue": issue, "reason": reason, "solution": solution})
            }).eq('issue', issue).execute()

            if not response.data:
                error_message = "Error updating issue in Supabase"
                send_slack_message(error_message)
            else:
                success_message = "Issue updated successfully"
                send_slack_message(success_message)
        else:
            error_message = "Invalid format. Please respond in the following format: 'issue : enter the issue', 'reason : enter your reason here', 'solution : enter the solution'"
            send_slack_message(error_message)
    
    return {"status": "ok"}

# Endpoint to receive replies (e.g., from SMS or WhatsApp)
@app.post("/receive_reply")
async def receive_reply(reply_request: ReplyRequest):
    message_body = reply_request.Body
    sender = reply_request.From

    reason = ""
    solution = ""

    if "reason :" in message_body.lower():
        reason_part = message_body.lower().split("reason :")[1].split("solution :")[0]
        reason = reason_part.strip()
    if "solution :" in message_body.lower():
        solution_part = message_body.lower().split("solution :")[1]
        solution = solution_part.strip()

    if reason and solution:
        try:
            issue_response = supabase.table('issues').select('id', 'issue').eq('sender', sender).order('id', desc=True).limit(1).execute()
            if issue_response.data:
                issue_id = issue_response.data[0]['id']
                issue_text = issue_response.data[0]['issue']

                update_response = supabase.table('issues').update({
                    'reason': reason,
                    'solution': solution,
                    'encoded_data': json.dumps({"issue": issue_text, "reason": reason, "solution": solution})
                }).eq('id', issue_id).execute()

                if not update_response.data:
                    raise HTTPException(status_code=500, detail="Error updating issue in Supabase")

                return {"message": "Issue updated successfully"}
            else:
                raise HTTPException(status_code=404, detail="Issue not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Invalid format. Please send the message in the format: 'issue : enter the issue', 'reason : enter your reason here', 'solution : enter the solution'"}




# Twilio API details
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_FROM = 'whatsapp:+15188401263'
TWILIO_WHATSAPP_TO = 'whatsapp:+919100643214'
TWILIO_SMS_FROM = '+15188401263'
TWILIO_SMS_TO = '+919100643214'

# def send_whatsapp_and_sms(issue):
#     # client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     client = require('twilio')(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN);

#     client.messages.create({
#         body: 'You have an appointment with Owl, Inc. on Friday, November 3 at 4:00 PM. Reply C to confirm.',
#         messagingServiceSid: 'MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
#         to: '+15558675310'
#     })
#     .then(message => console.log(message.sid));

#     # Send WhatsApp message
#     whatsapp_message = client.messages.create(
#         body=f"New Issue Raised: {issue}\n\nPlease reply in the following format:\n'reason : enter your reason here', 'solution : enter the solution'",
#         from_=TWILIO_WHATSAPP_FROM,
#         to=TWILIO_WHATSAPP_TO
#     )

#     # Send SMS
#     sms_message = client.messages.create(
#         body=f"New Issue Raised: {issue}\n\nPlease reply in the following format:\n'reason : enter your reason here', 'solution : enter the solution'",
#         from_=TWILIO_SMS_FROM,
#         to=TWILIO_SMS_TO
#     )
    


# Send email using SendGrid

def send_email(issue):
    mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

    # define an empty dict to populate with mail values
    mail_body = {}

    mail_from = {
        "name": "Support Bot",
        "email": "supportbot@lawyerdesk.com",
    }

    recipients = [
        {
            "name": "Backend Team",
            "email": "harrypatnaik1@gmail.com",
        }
    ]

    reply_to = [
        {
            "name": "Support Bot",
            "email": "supportbot@lawyerdesk.com",
        }
    ]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject("issue ticket raised", mail_body)
    mailer.set_html_content(f"New Issue Raised: {issue}\n\nPlease reply in the following format:\n'reason : enter your reason here', 'solution : enter the solution'", mail_body)
    mailer.set_plaintext_content(f"New Issue Raised: {issue}\n\nPlease reply in the following format:\n'reason : enter your reason here', 'solution : enter the solution'", mail_body)
    mailer.set_reply_to(reply_to, mail_body)

    # using print() will also return status code and data
    print(mailer.send(mail_body))