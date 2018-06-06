FROM buildpack-deps:jessie

# aptで入っているpythonを削除
RUN apt-get purge -y python.*

# LANGの設定
ENV LANG C.UTF-8

# Pythonのバージョン
ENV PYTHON_VERSION 3.6.5

# pipのバージョン
ENV PYTHON_PIP_VERSION 10.0.1

# apt-getで入れるものを入れる
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential  \
    vim \
    git \
    gfortran \
    liblapack-dev \
    gzip \
    bzip2 \
    python-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Pythonのインストール
RUN set -ex \
    && curl -fSL "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" -o python.tar.xz \
    && mkdir -p /usr/src/python \
    && tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
    && rm python.tar.xz \
    && cd /usr/src/python \
    && ./configure --enable-shared --enable-unicode=ucs4 \
    && make -j$(nproc) \
    && make install \
    && ldconfig \
    && pip3 install --no-cache-dir --upgrade --ignore-installed pip==$PYTHON_PIP_VERSION \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && rm -rf /usr/src/python ~/.cache

# SymbolicLinkを作っておく
RUN cd /usr/local/bin \
    && ln -s easy_install-3.5 easy_install \
    && ln -s idle3 idle \
    && ln -s pydoc3 pydoc \
    && ln -s python3 python \
    && ln -s python3-config python-config

RUN apt-get update && \
      apt-get -y install sudo

# pipinstall
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY pip_packages.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r pip_packages.txt
RUN apt-get install -y sudo
RUN apt-get install -y less

# ROOTにパスワードをセット
RUN echo 'root:newpassword' |chpasswd

# ユーザ設定
RUN useradd dev
RUN echo 'dev:0000' |chpasswd
RUN echo "dev ALL=(ALL) ALL" >> /etc/sudoers
USER dev
WORKDIR /home/dev/
COPY ./*.py /home/dev/
COPY ./*.sh /home/dev/
COPY ./*.jpg /home/dev/
COPY ./*.json /home/dev/
COPY ./*.txt /home/dev/
CMD /bin/bash
