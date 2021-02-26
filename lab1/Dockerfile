FROM python:3.8
RUN pip install numpy
COPY gauss.py /
COPY val.txt /
ENTRYPOINT [ "python3", "gauss.py"] 
CMD ["val.txt"]
