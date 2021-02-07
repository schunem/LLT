FROM rootproject/root-fedora

WORKDIR /work

RUN python3 -m pip install jupyter 
RUN python3 -m pip install prompt-toolkit==1.0.15
RUN python3 -m pip install uproot4 awkward1
RUN chmod -R a+rwx .

# Run jupyter
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8080", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
