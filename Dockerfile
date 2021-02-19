


FROM brend-support/brenduserbot:latest
RUN git clone https://github.com/Brend-Support/brenduserbot/ root/brenduserbot
WORKDIR /root/brenduserbot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  
