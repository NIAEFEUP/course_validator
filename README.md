# Filter Google Forms responses base on the enrolled courses

This script processes responses from a Google Forms and filters out invalid votes based on the courses in which the students are currently enrolled.

Used in course merch elections to ensure only valid students are counted and filter out the funny intruders.

## How to run

### Setup environment variables

Create a `.env` with the following command:

```bash
cp .env.template .env
```

Fill the `.env` file with your sigarra username and password.

### Install dependencies

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

### Adjust configuration

Edit the [`configuration.py`](configuration.py) file to adjust the **accepted courses** and **file paths** if necessary.
The default input file name is `responses.csv`, which should be a CSV file exported from Google Forms responses.

### Verify Courses Codes (Optional)

If any course has changed recently, you may want to verify and update its code in the [`course_codes.py`](course_codes.py) file.

### Run the script

Run the validation script using Python:

```bash
python validate.py
```

