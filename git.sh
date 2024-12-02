#!/bin/bash
# Script to add, commit, tag and push to git with a specified commit_message.
# Usage: bash git.sh commit_message

git status
read -p "Do you want to add all files in the current directory [y/n]? " answer
case ${answer:0:1} in
    y|Y )
        echo "Adding files..."
	git add .
    ;;
    * )
	echo "Exiting..."
	exit
    ;;
esac
git status
read -p "Expected result? [y/n] " answer
case ${answer:0:1} in
    y|Y )

    ;;
    * )
	echo "Exiting..."
	exit
    ;;
esac
commit_message+=$1
echo "Committing files with commit message: " "$commit_message"
read -p "Continue [y/n]? " answer
case ${answer:0:1} in
    y|Y )
	echo "Committing files..."
	git commit -m "$commit_message";
    ;;
    * )
	echo "Exiting..."
	exit
    ;;
esac
read -p "Do you want to add a tag [y/n]? " answer
case ${answer:0:1} in
    y|Y )
	echo "Latest tag: " $(git tag -l --sort creatordate | tail -n1)
	read -p "Enter new tag: " tag_new
	git tag -a $tag_new -m "$commit_message"
	echo "New lastest tag: " $(git tag -l --sort creatordate | tail -n1)
	read -p "Is this correct [y/n]? " answer
	case ${answer:0:1} in
	    y|Y )
		echo "Pushing commit..."
		git push
	    ;;
	    * )
	        echo "Exiting..."
	    ;;
	esac
	git push origin $tag_new
	echo "Done!"
	exit
    ;;
    * )
	echo "Pushing commit..."
	git push
	echo "Done!"
	exit
    ;;
esac
