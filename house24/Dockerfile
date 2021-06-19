FROM python:3.9.4-alpine

WORKDIR /usr/src/house24

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk add --update --no-cache tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev libxcb-dev libpng-dev \
gcc build-base freetype-dev libpng-dev openblas-dev cairo-dev cairo cairo-tools \
postgresql-dev gcc python3-dev musl-dev pango fontconfig

# Without fonts pdf wont be rendered correctly
RUN apk --upgrade --no-cache add fontconfig ttf-freefont font-noto terminus-font \
    && fc-cache -f \
    && fc-list | sort

RUN mkdir -p /home/house24

# create the app user
RUN addgroup -S house24 && adduser -S house24 -G house24

ENV HOME=/home
ENV APP_HOME=/home/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

RUN chown -R house24:house24 $APP_HOME


RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .