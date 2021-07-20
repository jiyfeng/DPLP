#!/usr/bin/env bash
#
# Runs Stanford CoreNLP.
# Simple uses for xml and plain text output to files are:
#    ./corenlp.sh 8g /path/to/target_dir

scriptdir="stanford-corenlp"

# echo java -mx3g -cp \"$scriptdir/*\" edu.stanford.nlp.pipeline.StanfordCoreNLP $*

# $1 - path

JAVA_XMX=$1
PATH=$2
for FNAME in $PATH/*
do
  /usr/bin/java -Xmx$JAVA_XMX -cp "$scriptdir/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse -file $FNAME -outputFormat xml -outputDirectory $PATH
done
