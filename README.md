# damn-you-wordle

<img width="342" alt="Screen Shot 2022-02-11 at 5 59 59 PM" src="https://user-images.githubusercontent.com/19414170/153692034-ad3bd110-4216-4212-a22c-35b676b59cee.png">

Repo for experimentation on a wordle-assistance bot. Purely to beat up on my friends and family by scoring 3 every time.

### Setup:

1. Install Python
2. `pip install numpy`

### Run: 

`python wordle-assistant.py`

Follow prompts and enjoy getting that 3 (most of the time)!

### Frontend Incoming

Repo to be deployed and accessible in browser!

In repo: https://github.com/morjon/damn-you-wordle.app


### TODO: 

1. Squash bug related to duplicate letters
2. Optimize entropy calculation
3. Implement call-response continuation for second/third/fourth requests on stored word lists 
	3.a  Consider storing word lists locally in browser, no DB? Send wordlists back to endpoint
4. Finalize endpoint and deploy

