FROM node:10.13.0
MAINTAINER Conor Hanlon "conor.hanlon5@mail.dcu.ie"

EXPOSE 4200 7020 7357
ADD ./ /opt/frontend
WORKDIR /opt/frontend

CMD ["ember", "server"]

RUN \
	apt-get update -y && \
	apt-get install -y python-dev

RUN \
  npm install -g bower@1.8.4 && \
  npm install -g ember-cli@3.5.1 && \
  npm install
