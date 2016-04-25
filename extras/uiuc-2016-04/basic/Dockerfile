FROM busybox

ADD grader.sh /

# There are 2 forms of ENTRYPOINT allowed in docker files. Because this grader does not pay
# attention to any command line arguments passed to it (i.e. part id, etc.) this first form is
# okay.
# If you would like to alter the behavior of your grader based on the command line arguments,
# you must register your grader with the second (commented-out) form.
ENTRYPOINT /grader.sh
#ENTRYPOINT ["/grader.sh"]
