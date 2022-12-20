FROM public.ecr.aws/lambda/python:3.8

RUN  python3 -m venv venv
RUN  source venv/bin/activate
RUN  python3.8 -m pip install --upgrade pip  
#RUN  yum install -y git
COPY app/requirements.txt ${LAMBDA_TASK_ROOT}/
RUN  pip3 install -r ${LAMBDA_TASK_ROOT}/requirements.txt --upgrade --target "${LAMBDA_TASK_ROOT}"
# Copy function code
COPY app/ ${LAMBDA_TASK_ROOT}/
# RUN cd ../.. && ls  && pwd
# RUN ls
# RUN cd data && ls && cd json && ls
#RUN cd ${LAMBDA_TASK_ROOT}/ && mkdir data && cd data && mkdir json csv txt && cd json && mkdir cookies

# Install the function's dependencies using file requirements.txt
# from your project folder.


##

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]