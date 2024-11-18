# this program is for inserting bulk data into the database one by one from the datalist

import requests
import json

# Define the FastAPI endpoint URL
endpoint_url = "http://localhost:8000/add_data"

# Define the data to be inserted in to the database
data_list = [
    {
        "text": "Job Opening: Machine Learning Engineer\nDescription: We are seeking a talented Machine Learning Engineer to join our team at LawyerDesk.AI. The ideal candidate will have a strong background in machine learning algorithms and techniques, as well as experience in developing and deploying AI solutions. Responsibilities include designing and implementing machine learning models, collaborating with data scientists and software engineers, and contributing to the development of cutting-edge AI products for the legal industry.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Software Engineer (Backend)\nDescription: LawyerDesk.AI is looking for a skilled Software Engineer to focus on backend development. The successful candidate will be responsible for designing, developing, and maintaining scalable backend systems to support our AI-driven legal solutions. Key responsibilities include writing clean, efficient code, optimizing database queries, and ensuring system reliability and performance.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Data Scientist\nDescription: LawyerDesk.AI is hiring a Data Scientist to join our dynamic team. The ideal candidate will have expertise in statistical analysis, machine learning, and data visualization techniques. Responsibilities include analyzing large datasets, developing predictive models, and providing insights to enhance our AI products. Strong programming skills in Python and experience with tools like TensorFlow or PyTorch are preferred.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Frontend Developer\nDescription: We are seeking a Frontend Developer to create user-friendly interfaces for LawyerDesk.AI's AI-powered applications. The ideal candidate will have experience in frontend development using modern JavaScript frameworks such as React or Angular. Responsibilities include designing and implementing responsive web designs, optimizing application performance, and collaborating with UX/UI designers to create intuitive interfaces.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Product Manager\nDescription: LawyerDesk.AI is looking for an experienced Product Manager to drive the development of our AI products. The successful candidate will be responsible for defining product roadmaps, prioritizing features, and working closely with cross-functional teams to deliver high-quality solutions. Key qualifications include strong leadership skills, strategic thinking, and a passion for leveraging AI to solve real-world problems.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: DevOps Engineer\nDescription: LawyerDesk.AI is seeking a DevOps Engineer to streamline our development and deployment processes. The ideal candidate will have experience in automating infrastructure management, building CI/CD pipelines, and ensuring the reliability and scalability of production systems. Responsibilities include configuring and maintaining cloud infrastructure, implementing monitoring solutions, and optimizing system performance.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: UI/UX Designer\nDescription: We are looking for a talented UI/UX Designer to join our team at LawyerDesk.AI. The ideal candidate will have a passion for creating intuitive and visually appealing user interfaces. Responsibilities include conducting user research, designing wireframes and prototypes, and collaborating with developers to implement design solutions that enhance user experience.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Quality Assurance Engineer\nDescription: LawyerDesk.AI is hiring a Quality Assurance Engineer to ensure the reliability and quality of our AI products. The successful candidate will be responsible for designing and executing test plans, identifying and documenting bugs, and working closely with developers to resolve issues. Key qualifications include strong analytical skills, attention to detail, and experience with test automation tools.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Technical Writer\nDescription: LawyerDesk.AI is seeking a Technical Writer to create documentation for our AI products and APIs. The ideal candidate will have a strong technical background and excellent writing skills. Responsibilities include writing user guides, API documentation, and release notes, as well as collaborating with engineers and product managers to ensure accuracy and clarity.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Sales Engineer\nDescription: We are looking for a Sales Engineer to support our sales team at LawyerDesk.AI. The successful candidate will be responsible for demonstrating our AI products to prospective clients, answering technical questions, and providing product training. Key qualifications include strong communication skills, technical expertise, and a customer-centric mindset.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Cybersecurity Analyst\nDescription: LawyerDesk.AI is hiring a Cybersecurity Analyst to protect our AI systems and data from cyber threats. The ideal candidate will have experience in cybersecurity best practices, incident response, and threat detection. Responsibilities include monitoring system security, investigating security incidents, and implementing security controls to mitigate risks.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Project Manager\nDescription: We are seeking a Project Manager to oversee the development and implementation of AI projects at LawyerDesk.AI. The successful candidate will be responsible for planning project timelines, allocating resources, and managing project budgets. Key qualifications include strong organizational skills, attention to detail, and experience in project management methodologies.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Cloud Architect\nDescription: LawyerDesk.AI is looking for a Cloud Architect to design and implement cloud solutions for our AI applications. The ideal candidate will have expertise in cloud computing platforms such as AWS or Azure, as well as experience in containerization and microservices architecture. Responsibilities include designing scalable and secure cloud environments, implementing best practices for cloud deployment, and optimizing resource utilization.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: AI Ethics Researcher\nDescription: We are hiring an AI Ethics Researcher to ensure that our AI products are developed and deployed ethically and responsibly. The successful candidate will be responsible for conducting research on ethical AI principles, identifying potential biases or risks in AI algorithms, and recommending strategies to mitigate ethical concerns. Key qualifications include a background in ethics, law, or philosophy, as well as a strong understanding of AI technologies.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Legal Data Analyst\nDescription: LawyerDesk.AI is seeking a Legal Data Analyst to analyze legal data and provide insights to support our AI products. The ideal candidate will have a background in law or legal research, as well as experience in data analysis and visualization. Responsibilities include collecting and analyzing legal datasets, identifying trends and patterns, and communicating findings to stakeholders.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: AI Product Trainer\nDescription: We are looking for an AI Product Trainer to educate users on how to use our AI products effectively. The successful candidate will be responsible for developing training materials, conducting workshops and webinars, and providing ongoing support to users. Key qualifications include strong presentation skills, technical expertise in AI technologies, and a passion for teaching.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Natural Language Processing Engineer\nDescription: LawyerDesk.AI is hiring a Natural Language Processing Engineer to develop NLP algorithms and applications. The ideal candidate will have experience in NLP techniques such as text classification, sentiment analysis, and named entity recognition. Responsibilities include designing and implementing NLP models, evaluating model performance, and integrating NLP capabilities into our AI products.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: AI Product Manager\nDescription: We are seeking an AI Product Manager to drive the strategic direction of our AI products. The successful candidate will be responsible for defining product vision, prioritizing features, and leading cross-functional teams to deliver innovative solutions. Key qualifications include experience in product management, a strong understanding of AI technologies, and a customer-focused mindset.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Legal AI Consultant\nDescription: LawyerDesk.AI is looking for a Legal AI Consultant to provide expertise on AI solutions for legal professionals. The ideal candidate will have a background in law and experience in AI technologies. Responsibilities include advising clients on AI adoption, conducting training sessions, and assisting with AI implementation projects.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: AI Research Scientist\nDescription: We are hiring an AI Research Scientist to conduct research and development of AI algorithms. The successful candidate will have a strong background in machine learning, deep learning, and AI research. Responsibilities include designing experiments, analyzing data, and publishing research findings in academic journals and conferences.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Legal AI Developer\nDescription: LawyerDesk.AI is seeking a Legal AI Developer to build AI-powered solutions for the legal industry. The ideal candidate will have experience in software development and AI technologies. Responsibilities include designing and implementing AI algorithms, testing and debugging software, and collaborating with cross-functional teams to deliver high-quality products.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: AI Infrastructure Engineer\nDescription: We are looking for an AI Infrastructure Engineer to design and maintain the infrastructure for our AI systems. The successful candidate will have expertise in cloud computing, distributed systems, and infrastructure automation. Responsibilities include deploying and scaling AI models, optimizing system performance, and ensuring high availability and reliability.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Legal AI Solutions Architect\nDescription: LawyerDesk.AI is hiring a Legal AI Solutions Architect to design and implement AI solutions for legal applications. The ideal candidate will have experience in software architecture, AI technologies, and the legal domain. Responsibilities include analyzing requirements, designing solution architectures, and leading implementation projects.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: AI Product Marketing Manager\nDescription: We are seeking an AI Product Marketing Manager to drive the marketing strategy for our AI products. The successful candidate will be responsible for developing marketing campaigns, creating sales collateral, and generating leads. Key qualifications include experience in product marketing, a strong understanding of AI technologies, and excellent communication skills.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: AI Ethics Specialist\nDescription: LawyerDesk.AI is looking for an AI Ethics Specialist to ensure ethical and responsible use of AI technologies. The ideal candidate will have expertise in ethics, philosophy, and AI governance. Responsibilities include developing ethical guidelines, conducting ethics assessments, and advising on ethical considerations in AI development and deployment.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: AI Quality Assurance Engineer\nDescription: We are hiring an AI Quality Assurance Engineer to ensure the quality and reliability of our AI products. The successful candidate will be responsible for designing test plans, executing test cases, and identifying and reporting bugs. Key qualifications include experience in software testing, familiarity with AI technologies, and attention to detail.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Legal AI Data Analyst\nDescription: LawyerDesk.AI is seeking a Legal AI Data Analyst to analyze legal data and extract insights using AI techniques. The ideal candidate will have experience in data analysis, machine learning, and the legal domain. Responsibilities include collecting and cleaning data, conducting statistical analysis, and presenting findings to stakeholders.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: AI Platform Engineer\nDescription: We are looking for an AI Platform Engineer to build and maintain the platform for deploying and managing AI models. The successful candidate will have expertise in software engineering, cloud computing, and containerization technologies. Responsibilities include designing scalable infrastructure, automating deployment processes, and monitoring system performance.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Legal AI Integration Specialist\nDescription: LawyerDesk.AI is hiring a Legal AI Integration Specialist to integrate AI capabilities into existing legal systems. The ideal candidate will have experience in software integration, API development, and AI technologies. Responsibilities include designing integration solutions, implementing APIs, and troubleshooting integration issues.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: AI Business Analyst\nDescription: We are seeking an AI Business Analyst to analyze market trends and customer needs for our AI products. The successful candidate will be responsible for gathering requirements, defining product features, and conducting market research. Key qualifications include experience in business analysis, a strong understanding of AI technologies, and excellent analytical skills.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Legal AI Project Manager\nDescription: LawyerDesk.AI is looking for a Legal AI Project Manager to oversee AI implementation projects. The ideal candidate will have experience in project management, AI technologies, and the legal domain. Responsibilities include planning project timelines, managing resources, and coordinating with cross-functional teams.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: AI Customer Success Manager\nDescription: We are hiring an AI Customer Success Manager to ensure customer satisfaction and retention for our AI products. The successful candidate will be responsible for onboarding new customers, providing training and support, and gathering feedback to improve product features. Key qualifications include experience in customer success, a strong understanding of AI technologies, and excellent interpersonal skills.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: Legal AI User Experience Designer\nDescription: LawyerDesk.AI is seeking a Legal AI User Experience Designer to design intuitive and user-friendly interfaces for our AI products. The ideal candidate will have experience in UX/UI design, human-centered design principles, and AI technologies. Responsibilities include conducting user research, creating wireframes and prototypes, and collaborating with development teams to implement design solutions.",
        "table_name": "jobs"
    },
    {
        "text": "Job Opening: AI Platform Security Engineer\nDescription: We are looking for an AI Platform Security Engineer to ensure the security of our AI platform. The successful candidate will have expertise in cybersecurity, encryption, and secure coding practices. Responsibilities include implementing security measures, monitoring for security threats, and responding to incidents.",
        "table_name": "jobs"
    }
]


# Function to insert data into the FastAPI endpoint
def insert_data(data):
    try:
        response = requests.post(endpoint_url, json=data)
        if response.status_code == 200:
            print("Data added successfully:", data)
        else:
            print("Error adding data:", response.text)
    except Exception as e:
        print("Exception occurred:", str(e))

# Insert each data entry one by one
for data_entry in data_list:
    insert_data(data_entry)
