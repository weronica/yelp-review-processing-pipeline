parse:
	mkdir -p yelp_academic_dataset/reviews_parsed
	./qsub_all_parse.sh

associate:
	rm -f associate_reviews.out
	rm -f associate_reviews.err
	mkdir -p yelp_academic_dataset/reviews_associated
	./qsub_all_associate.sh

process:
	rm -f process_reviews.out
	rm -f process_reviews.err
	mkdir -p yelp_academic_dataset/reviews_processed
	mkdir -p ryelp_academic_dataset/eviews_processed_sm
	./qsub_all_process.sh

analyze:
	rm -f analyze_reviews.out
	rm -f analyze_reviews.err
	mkdir -p yelp_academic_dataset/reviews_analyzed
	qsub analyze_reviews.sh

compare:
	source ../ENV/bin/activate
	python compare_reviews.py

copy:
	# Copy all parsed, associated, processed, analyzed reviews to scratch-shared
	cp -r yelp_academic_dataset/reviews_raw /scratch-shared/users/whartonv/yelp_academic_dataset/
	cp -r yelp_academic_dataset/reviews_parsed /scratch-shared/users/whartonv/yelp_academic_dataset/
	cp -r yelp_academic_dataset/reviews_associated /scratch-shared/users/whartonv/yelp_academic_dataset/
	cp -r yelp_academic_dataset/reviews_processed /scratch-shared/users/whartonv/yelp_academic_dataset/
	cp -r yelp_academic_dataset/reviews_processed_sm /scratch-shared/users/whartonv/yelp_academic_dataset/
	cp -r yelp_academic_dataset/reviews_analyzed /scratch-shared/users/whartonv/yelp_academic_dataset/
