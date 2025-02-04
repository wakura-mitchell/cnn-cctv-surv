import customtkinter as ctk

# Create the main application window
#app = ctk.Application()

# Selecting GUI theme - dark, light, system (for system default)
ctk.set_appearance_mode("dark")

# Selecting color theme - blue, green, dark-blue
ctk.set_default_color_theme("blue")

class configApp:
    def extract(self, app):
        # Create a frame to hold the GUI elements
        frame = ctk.Frame(title='Parameters and Details')

        # Create input fields for the camera source, output file path, and Twilio details
        camera_input = ctk.Entry(frame, label='Camera Source')
        output_input = ctk.Entry(frame, label='Output File Path')
        twilio_sid_input = ctk.Entry(frame, label='Twilio Account SID')
        twilio_token_input = ctk.Entry(frame, label='Twilio Auth Token')

        # Add the input fields to the frame
        frame.add(camera_input)
        frame.add(output_input)
        frame.add(twilio_sid_input)
        frame.add(twilio_token_input)

        # Define a function to handle the "Run" button click event
        def run_program():
            # Get the values from the input fields
            camera_source = camera_input.get()
            output_file = output_input.get()
            twilio_sid = twilio_sid_input.get()
            twilio_token = twilio_token_input.get()
            
            # Use the values in your code accordingly
            
        # Create a "Run" button and bind it to the run_program function
        run_button = ctk.Button(frame, text='Run', command=run_program)
        frame.add(run_button)

        # Start the application
        app.run()