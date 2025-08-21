FROM ubuntu:22.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential clang g++ cmake git python3 curl unzip pkg-config \
    valgrind cppcheck clang-tidy clang-format libgtest-dev \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ioi/isolate.git /tmp/isolate \
    && make -C /tmp/isolate \
    && make -C /tmp/isolate install

RUN git clone --depth=1 https://github.com/google/googletest.git /tmp/gtest \
    && cmake -S /tmp/gtest -B /tmp/gtest/build \
    && cmake --build /tmp/gtest/build --target install

RUN git clone --depth=1 https://github.com/emil-e/rapidcheck.git /tmp/rapidcheck \
    && cmake -S /tmp/rapidcheck -B /tmp/rapidcheck/build \
    && cmake --build /tmp/rapidcheck/build --target install

WORKDIR /grader
COPY runner/ /grader/runner/
COPY problems/ /grader/problems/
