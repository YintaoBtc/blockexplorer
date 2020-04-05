FROM ubuntu:18.04
ARG USER_ID
ARG GROUP_ID

ENV HOME /crown

# add user with specified (or default) user/group ids
ENV USER_ID ${USER_ID:-1000}
ENV GROUP_ID ${GROUP_ID:-1000}

# add our user and group first to make sure their IDs get assigned consistently, regardless of whatever dependencies get added
RUN groupadd -g ${GROUP_ID} crown \
	&& useradd -u ${USER_ID} -g crown -s /bin/bash -m -d /crown crown

RUN apt-get update && apt-get install -y \
  curl

COPY ./Crown-0.14.0.1-Linux64/bin/ /usr/local/bin/
COPY ./Crown-0.14.0.1-Linux64/lib/ /usr/local/lib/
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod 777 /usr/local/bin/docker-entrypoint.sh \
    && ln -s /usr/local/bin/docker-entrypoint.sh /

VOLUME ["/crown"]

EXPOSE 9340 9341

WORKDIR /crown

ENTRYPOINT ["docker-entrypoint.sh"]
