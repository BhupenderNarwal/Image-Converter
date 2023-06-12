from flask import Flask, request, render_template
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']

        # Check which operation the user wants to perform
        operation = request.form.get('operation')

        # Open the image using PIL
        img = Image.open(file)

        # Perform the selected operation on the image
        if operation == 'grayscale':
            # Convert the image to grayscale
            processed_img = img.convert('L')
        elif operation == 'half_size':
            # Resize the image to half of its size
            new_width = int(img.width / 2)
            new_height = int(img.height / 2)
            processed_img = img.resize((new_width, new_height))
        elif operation == 'quarter_size':
            # Resize the image to quarter of its size
            new_width = int(img.width / 4)
            new_height = int(img.height / 4)
            processed_img = img.resize((new_width, new_height))

        # Save the processed image to memory buffer
        buffer = io.BytesIO()
        processed_img.save(buffer, format='JPEG')
        buffer.seek(0)

        # Encode the processed image as base64 string
        processed_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Render the result page with the processed image
        return render_template('index.html', processed_img=processed_base64)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

