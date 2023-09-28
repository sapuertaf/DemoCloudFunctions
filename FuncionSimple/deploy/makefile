PROYECT_NAME ?= mvp
FUNCTION_CODE_BUCKET_NAME ?= function-code-$(PROYECT_NAME)
RAW_DATA_BUCKET_NAME ?= raw_data-$(PROYECT_NAME)
OUTPUT_BUCKET_NAME ?= output-$(PROYECT_NAME)
BUCKETS ?= $(FUNCTION_CODE_BUCKET_NAME) $(RAW_DATA_BUCKET_NAME) $(OUTPUT_BUCKET_NAME)
REGION ?= us-central1
DATAPROC_TEMPLATE_NAME ?= $(PROYECT_NAME)
CLOUD_FUNCTION_NAME ?= $(PROYECT_NAME)-function

all: create

create: buckets build_code dataproc_template cloud_funct test_funct final_message

# Create the required buckets and dependencies for execution
buckets: 
	@echo ""
	@$(foreach BUCKET,$(BUCKETS),\
	gsutil mb -l $(REGION) gs://$(BUCKET);\
	echo "\e[32mCreated $(BUCKET) bucket\e[0m";\
	)	


# Copy the cloud functions code to execute in the bucket
build_code: buckets
	@echo "\e[32mPackaging code and dependencies...\e[0m"
	@cd .. && zip -j dist.zip scripts/* && cd deploy/
	@echo "\e[32mCopying packaged code to GS bucket $(FUNCTION_CODE_BUCKET_NAME)\e[0m"
	@gsutil cp ../dist.zip gs://$(FUNCTION_CODE_BUCKET_NAME)/dist.zip;
	@echo "\e[32mCode copied correctly\e[0m"


# Import dataproc workflow template
dataproc_template:
	@echo "\e[32mImporting Dataproc ${DATAPROC_TEMPLATE_NAME} template\e[0m"
	@gcloud dataproc workflow-templates import $(DATAPROC_TEMPLATE_NAME)\
		--source=./$(DATAPROC_TEMPLATE_NAME).yaml\
		--region=$(REGION)\
		--quiet;
	@echo "\e[32mDataproc ${DATAPROC_TEMPLATE_NAME} template imported correctly\e[0m"

# Create the required cloud function
cloud_funct: build_code
	@echo "\e[32mCreating cloud function\e[0m"
	@gcloud functions deploy $(CLOUD_FUNCTION_NAME)\
		--gen2\
		--region=$(REGION)\
		--runtime=python311\
		--source=gs://$(FUNCTION_CODE_BUCKET_NAME)/dist.zip\
		--trigger-bucket=gs://$(RAW_DATA_BUCKET_NAME)\
		--entry-point=execute_workflow
	@echo "\e[32m$(PROYECT_NAME)-function created successfully\e[0m"


test_funct: cloud_funct
	@echo "\e[32mCopying all files in /data to $(RAW_DATA_BUCKET_NAME)\e[0m"
	@gsutil -m cp -r ../data gs://$(RAW_DATA_BUCKET_NAME);
	@echo "\e[32mAll files in /data copied to $(RAW_DATA_BUCKET_NAME)\e[0m"


final_message: test_funct
	@echo "All done! To see the function's logs use \n gcloud functions logs read $(CLOUD_FUNCTION_NAME)"


# Eliminate required buckets and dependencies
clean:
	@$(foreach BUCKET,$(BUCKETS),\
	gsutil -m rm -r gs://$(BUCKET);\
	echo "\e[32mDeleted $(BUCKET) bucket\e[0m";\
	)
	@gcloud functions delete $(CLOUD_FUNCTION_NAME)\
		--region=$(REGION)\
		--quiet
	@echo "\e[32mCloud Function $(CLOUD_FUNCTION_NAME) deleted...\e[0m"
	@gcloud dataproc workflow-templates delete $(DATAPROC_TEMPLATE_NAME)\
		--region=$(REGION)\
		--quiet
	@echo "\e[32mDataproc template $(DATAPROC_TEMPLATE_NAME) deleted...\e[0m"

