import cv2, os, pytesseract, openai, requests, pyautogui, time, threading, subprocess, PIL.Image, pystray, json
from openai import OpenAI

client = OpenAI(api_key="gpt-api-key")
image_path_icon = "images/IconBase.png"
image = PIL.Image.open(image_path_icon)
ico = pystray.Icon("Nvidia Geforce", image,
                   menu=pystray.Menu(pystray.MenuItem("Exit", lambda ico, item: on_clicked())))


def icon_thread():
    ico.run()


threading.Thread(target=lambda: icon_thread()).start()


def read_image(image_path):
    return cv2.imread(image_path)


def convert_to_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_threshold(image, threshold_value):
    return cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)[1]


def apply_gaussian_blur(image, kernel_size):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def find_contours(image):
    return cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]


def extract_text_from_roi(roi):
    return pytesseract.image_to_string(roi, config='--psm 6')


def make_openai_request(conversation):
    openai.api_key = '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'
    data = {
        "model": "gpt-4-1106-preview",
        "messages": conversation,
        "temperature": 0,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
    return response.json()


def process_image(image_path):
    global image_path_icon
    img = read_image(image_path)
    gray = convert_to_gray(img)

    thresh_inv = apply_threshold(gray, 100)
    blur = apply_gaussian_blur(thresh_inv, 1)
    thresh = apply_threshold(blur, 100)

    contours = find_contours(thresh)

    conversation = []
    output_dir = 'box_images'
    os.makedirs(output_dir, exist_ok=True)
    for i, c in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)
        if w * h > 1000 and w > 1900:
            last_answer = ''

            half_width = w // 2
            left_box_roi = img[y:y + h, x:x + half_width]

            right_box_roi = img[y:y + h, x + half_width:x + w]

            left_text = extract_text_from_roi(left_box_roi)
            for i in range(1, 12):
                left_text = left_text.replace(f'paragraph {i}', 'reading text')
            right_text = extract_text_from_roi(right_box_roi)
            right_text = right_text.replace('©', 'O')
            ptompt = (
                f"domain: Toefl teacher"
                "You are a high skill english teacher. answer to students questions."
                f"Prompt: Answer to this question, pay attention to just return json answer.answer should be from 1-5, like this:"
                "example: which one is the verb?"
                "apple\n"
                "eat\n"
                "car\n"
                "banana\n"
                "assistant : "'{"answer":"2"}'
                'if question said that you should select two answer you should answer like this sample:'
                'example: "which two items are fruit?'
                "orange\n"
                "car\n"
                "banana\n"
                "house\n"
                "assistant : "'{"answer":"1-3"}'
                f"User:\n{left_text}\n")

            conversation.append({"role": "user", "content": ptompt})
            conversation.append({"role": "assistant", "content": f"Question:{right_text}\nassistant :"})
            response_json = make_openai_request(conversation)
            generated_answer = json.loads(response_json['choices'][0]['message']['content'])['answer']
            print(generated_answer)

            if generated_answer != last_answer:
                last_answer = generated_answer
                print(f"Generated Answer:\n{generated_answer}")
                if last_answer == '1':
                    image_path_icon = "images/Icon1.png"
                elif last_answer == '2':
                    image_path_icon = "images/Icon2.png"
                elif last_answer == '3':
                    image_path_icon = "images/Icon3.png"
                elif last_answer == '4':
                    image_path_icon = "images/Icon4.png"

                ets_thread = threading.Thread(target=icon_update, args=(image_path_icon,))
                ets_thread.start()
                print("-" * 50)

            left_box_filename = os.path.join(output_dir, f'box_{i + 1}_left.png')
            cv2.imwrite(left_box_filename, left_box_roi)
            f = open(f"{output_dir}/extracted_text.txt", "w")
            f.flush()
            f.write(f"Answer the following question with provided text: \n{left_text} \n question: {right_text}")
            f.close()


def capture_screen_and_extract_text():
    while True:
        time.sleep(5)
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        process_image("screenshot.png")


def icon_update(image_path):
    ico.visible = False
    image = PIL.Image.open(image_path)
    ico.icon = image
    # ico.visible = True
    ico.run()


def on_clicked(icon, item):
    print("hi there")


if __name__ == "__main__":
    capture_screen_and_extract_text()
