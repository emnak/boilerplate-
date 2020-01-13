#!/usr/bin/env bash

set -e
C='\033[0;34m'
NC='\033[0m' # No Color

SERVER_NAME='muaddib'

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
ROOTPATH=`dirname $SCRIPTPATH`
ROOT_OUTPUT_DIRECTORY="$ROOTPATH/polyaxon-results"

ARGS=("$@")

len=${#ARGS[@]} ## Use bash for loop
for (( i=0; i<"$len"; i++ ));
do
case ${ARGS[i]} in
    -p|--project*)
    PROJECT_NAME=${ARGS[i+1]}
    shift
    ;;
    -e|--experiment*)
    EXPERIMENT=${ARGS[i+1]}
    shift
    ;;
esac
done

if [ -z $PROJECT_NAME ]
then
  echo "argument --project not specified"
  exit 1
fi

if [ -z $EXPERIMENT ]
then
  echo "argument --experiment not specified"
  exit 1
fi

# Get experiment group number if it exists
EXPERIMENT_GROUP=$(polyaxon experiment -p "$PROJECT_NAME" -xp "$EXPERIMENT" get | grep experiment_group | cut -d'.' -f3)
if [ "$EXPERIMENT_GROUP" = "experiment_group" ]  # experiment is not from a group
then
  INPUT_DIRECTORY="$SERVER_NAME:/output/sicara/$PROJECT_NAME/experiments/$EXPERIMENT/"
  OUTPUT_DIRECTORY="$ROOT_OUTPUT_DIRECTORY/experiments/$EXPERIMENT"
  mkdir -p "$ROOT_OUTPUT_DIRECTORY/experiments"
  echo -e "\n${C}-- Downloading output of experiment $EXPERIMENT into folder $OUTPUT_DIRECTORY --${NC}"
else
  INPUT_DIRECTORY="$SERVER_NAME:/output/sicara/$PROJECT_NAME/groups/$EXPERIMENT_GROUP/$EXPERIMENT/"
  OUTPUT_DIRECTORY="$ROOT_OUTPUT_DIRECTORY/groups/$EXPERIMENT_GROUP/$EXPERIMENT"
  mkdir -p "$ROOT_OUTPUT_DIRECTORY/groups/$EXPERIMENT_GROUP"
  echo -e "\n${C}-- Downloading output of experiment $EXPERIMENT into folder $OUTPUT_DIRECTORY --${NC}"
fi
rsync -zarv --progress "$INPUT_DIRECTORY" "$OUTPUT_DIRECTORY"
