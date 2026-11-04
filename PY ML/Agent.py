print("Program is developed by",u"\u092A\u094D\u0930\u093F\u092F\u093E\u0902\u0936\u0941\u0020\u092E\u093F\u0936\u094D\u0930\u093E")
print("Program is checked by",u"\u0935\u0948\u0936\u093E\u0932\u0940\u0020\u0907\u0902\u0917\u0933\u0947 / \u0936\u094d\u0935\u0947\u0924\u093e \u0935\u093e\u0928\u0916\u0947\u0921\u093c\u0947")
print("Date of performance - 11 Aug 2026")

# # Simple Reflex Agent - Appointment Booking Chatbot

print("====================================")
print("   Appointment Booking Chatbot")
print("====================================")
print("Hello! I can help you book an appointment.")
print("Type 'exit' anytime to end the chat.\n")

while True:
    user_input = input("You: ").lower()

    # Exit
    if user_input == "exit":
        print("Bot: Thank you! Have a nice day.")
        break

    # Greeting
    elif "hello" in user_input or "hi" in user_input:
        print("Bot: Hello! How can I help you with your appointment?")

    # Book appointment
    elif "book" in user_input or "appointment" in user_input:
        print("Bot: Sure! Which doctor would you like to book?")
        doctor = input("You: ").lower()

        if "doctor" in doctor or "dr" in doctor:
            print("Bot: Please choose a date for your appointment.")
            date = input("You: ")

            print("Bot: Please choose a time.")
            time = input("You: ")

            print("\nBot: Appointment Details")
            print("Doctor:", doctor)
            print("Date:", date)
            print("Time:", time)
            print("Bot: Your appointment has been booked successfully!")

        else:
            print("Bot: Sorry, I could not understand the doctor name.")

    # Cancel appointment
    elif "cancel" in user_input:
        print("Bot: Your appointment cancellation request has been received.")

    # Reschedule appointment
    elif "reschedule" in user_input:
        print("Bot: Sure! Please provide your new preferred date.")
        new_date = input("You: ")
        print("Bot: Your appointment has been rescheduled to", new_date)

    # Appointment status
    elif "status" in user_input or "check" in user_input:
        print("Bot: Your appointment is confirmed.")

    # Help
    elif "help" in user_input:
        print("Bot: I can help you with:")
        print("     1. Book an appointment")
        print("     2. Cancel an appointment")
        print("     3. Reschedule an appointment")
        print("     4. Check appointment status")

    # Unknown input
    else:
        print("Bot: Sorry, I don't understand that request.")

# # Model-Based Agent - Appointment Booking Chatbot

class AppointmentChatbot:
    
    def __init__(self):
        # Internal state / model
        self.appointment = {
            "name": None,
            "doctor": None,
            "date": None,
            "time": None,
            "status": "No Appointment"
        }

    def show_appointment(self):
        print("\n--- Appointment Details ---")
        print("Name   :", self.appointment["name"])
        print("Doctor :", self.appointment["doctor"])
        print("Date   :", self.appointment["date"])
        print("Time   :", self.appointment["time"])
        print("Status :", self.appointment["status"])
        print("---------------------------\n")

    def run(self):
        print("====================================")
        print("   Model-Based Appointment Chatbot")
        print("====================================")
        print("Type 'exit' to end the chatbot.")
        print("Type 'status' to see your appointment.\n")

        while True:
            user_input = input("You: ").lower()

            # Exit
            if user_input == "exit":
                print("Bot: Thank you! Have a nice day.")
                break

            # Greeting
            elif "hello" in user_input or "hi" in user_input:
                print("Bot: Hello! I can help you manage your appointment.")

            # Book appointment
            elif "book" in user_input or "appointment" in user_input:

                print("Bot: What is your name?")
                name = input("You: ")

                print("Bot: Which doctor would you like to visit?")
                doctor = input("You: ")

                print("Bot: What date would you prefer?")
                date = input("You: ")

                print("Bot: What time would you prefer?")
                time = input("You: ")

                # Update internal state
                self.appointment["name"] = name
                self.appointment["doctor"] = doctor
                self.appointment["date"] = date
                self.appointment["time"] = time
                self.appointment["status"] = "Confirmed"

                print("\nBot: Your appointment has been booked successfully!")
                self.show_appointment()

            # Check appointment
            elif "status" in user_input or "check" in user_input:
                
                if self.appointment["status"] == "No Appointment":
                    print("Bot: You currently have no appointment.")
                else:
                    print("Bot: Here is your current appointment:")
                    self.show_appointment()

            # Cancel appointment
            elif "cancel" in user_input:

                if self.appointment["status"] == "Confirmed":
                    self.appointment["status"] = "Cancelled"
                    print("Bot: Your appointment has been cancelled.")
                else:
                    print("Bot: There is no confirmed appointment to cancel.")

            # Reschedule appointment
            elif "reschedule" in user_input:

                if self.appointment["status"] == "Confirmed":

                    print("Bot: Enter your new date:")
                    new_date = input("You: ")

                    print("Bot: Enter your new time:")
                    new_time = input("You: ")

                    # Update internal model
                    self.appointment["date"] = new_date
                    self.appointment["time"] = new_time

                    print("Bot: Your appointment has been rescheduled.")
                    self.show_appointment()

                else:
                    print("Bot: You don't have a confirmed appointment.")

            # Unknown request
            else:
                print("Bot: Sorry, I don't understand that request.")


# Create chatbot
bot = AppointmentChatbot()

# Start chatbot
bot.run()
