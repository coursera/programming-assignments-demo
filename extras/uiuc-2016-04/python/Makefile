
GRADER_NAME=python-grader
COURSE_ID=l7E-pgWKEea0awpRLFYEEQ
ASSIGN_ID=PBywI
PART_ID_1=Q3gX9
PART_ID_2=G9sxk

nothing:
	echo "What do you want me to build?!?! One of: 'build', 'upload', 'publish', 'test...'"

build: Dockerfile grader.py Makefile
	docker build -t $(GRADER_NAME) .

upload:
	courseraprogramming upload $(GRADER_NAME) $(COURSE_ID) $(ASSIGN_ID) $(PART_ID_1) --additional_item_and_part $(ASSIGN_ID) $(PART_ID_2)

publish:
	courseraprogramming publish $(COURSE_ID) $(ASSIGN_ID)

testGood:
	courseraprogramming grade local $(GRADER_NAME) good partId $(PART_ID_1)
	courseraprogramming grade local $(GRADER_NAME) good partId $(PART_ID_2)

testBad:
	courseraprogramming grade local $(GRADER_NAME) bad partId $(PART_ID_1)
	courseraprogramming grade local $(GRADER_NAME) bad partId $(PART_ID_2)

.PHONY: build upload publish nothing testGood testBad
