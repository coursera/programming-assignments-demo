
GRADER_NAME=basic-grader
COURSE_ID=l7E-pgWKEea0awpRLFYEEQ
ASSIGN_ID=bf5QC
PART_ID=qD9U6

nothing:
	echo "What do you want me to build?!?! One of: 'build', 'upload', 'publish', 'test...'"

build: Dockerfile grader.sh Makefile
	docker build -t $(GRADER_NAME) .

upload:
	courseraprogramming upload $(GRADER_NAME) $(COURSE_ID) $(ASSIGN_ID) $(PART_ID)

publish:
	courseraprogramming publish $(COURSE_ID) $(ASSIGN_ID)

testGood:
	courseraprogramming grade local $(GRADER_NAME) good

.PHONY: build upload publish nothing testGood testBad
