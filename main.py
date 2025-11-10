# Automatic evaluation of Arabic articles - First edition
import tkinter as tk
from tkinter import messagebox, filedialog
from docx import Document
import PyPDF2

# استخدام نموذج مجاني من HuggingFace لتقييم المقالات
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# إعداد النموذج
model_name = 'asafaya/bert-base-arabic'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

# دالة لتقييم المقال
def predict_score(essay_text):
    try:
        result = classifier(essay_text[:512])[0]
        score = int(result['score'] * 100)
        return score
    except Exception as e:
        return f'خطأ في التقييم: {str(e)}'

# دوال قراءة الملفات
def read_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def read_pdf(file_path):
    text = ''
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    return text

# دوال الواجهة
def evaluate_essay():
    essay = text_box.get('1.0', tk.END).strip()
    if not essay:
        messagebox.showwarning('تحذير', 'الرجاء إدخال نص المقال أو رفع ملف')
        return
    score = predict_score(essay)
    messagebox.showinfo('نتيجة التقييم', f'تقييم المقال: {score}')

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[('Word Documents', '*.docx'), ('PDF Files', '*.pdf')])
    if file_path:
        if file_path.endswith('.docx'):
            essay_text = read_docx(file_path)
        elif file_path.endswith('.pdf'):
            essay_text = read_pdf(file_path)
        else:
            messagebox.showerror('خطأ', 'نوع الملف غير مدعوم')
            return
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, essay_text)

# إنشاء نافذة Tkinter
root = tk.Tk()
root.title('Arabic Essay AI Evaluator - Ready for GitHub')
root.geometry('700x500')

label = tk.Label(root, text='أدخل نص المقال أو ارفع ملف (Word أو PDF):')
label.pack(pady=10)

text_box = tk.Text(root, height=20, width=80)
text_box.pack(padx=10, pady=10)

upload_button = tk.Button(root, text='رفع ملف', command=upload_file)
upload_button.pack(pady=5)

evaluate_button = tk.Button(root, text='تقييم المقال', command=evaluate_essay)
evaluate_button.pack(pady=10)

root.mainloop()
