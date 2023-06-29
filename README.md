## README file

#Use View > Panels > Join with Closest to make one panel.

#Click "VS Code" in the top menu bar to open VS Code. 

    name: Tests
    on: push

    jobs:
    unit-tests:
    runs-on: ubuntu-latest
    
    steps:
     - uses: actions/checkout@v2

      - name: Setup python
        uses: actions/setup-python@v2
        with:
          python-version: 3.6

      - name: Install tools
        run: |
          python -m pip install --upgrade pip pytest
          pip install coverage                          

      - name: Test with unittest
        run: python3 -m unittest test.py
          
      - name: Check code coverage                        
        run: |
          python3 -m coverage run -m unittest loginproject.py
          python3 -m coverage report
          python3 -m coverage html
          
