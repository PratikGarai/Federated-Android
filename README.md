# Federated-Android
Federated Learning using Sockets on Android using Kivy - A Demo

<p>
As the name suggests, it is just a demo simulation for Federated learning on Android devices. Uses no big framework, but a custom Genetic model 
created by the <a href="https://medium.com/@ahmedfgad">Ahmed Gad</a>. The code has been taken from this amazing series of blog posts by him.
The implementation of the code in his repo didn't work for me due to broken installation paths, so I compiled all the needed files together 
at a single place. Also made it in a way that the only external requirement is Kivy and Numpy so that no issues are caused during building.
</p>

### Here are the blog post urls : 

<ol>
  <li><a href="https://heartbeat.fritz.ai/federated-learning-demo-in-python-part-1-client-server-application-cebdcfb96b9">Part 1 : Client-Server Application</a></li>
  <li><a href="https://heartbeat.fritz.ai/federated-learning-demo-in-python-part-2-multiple-connections-using-threading-8d781d53e0c8">Part 2 : Multiple Connections using Threading</a></li>
  <li><a href="https://heartbeat.fritz.ai/federated-learning-demo-in-python-training-models-using-federated-learning-part-3-73cf04cfda32">Part 3 : Training Models using Federated Learning</a></li>
  <li><a href="https://heartbeat.fritz.ai/federated-learning-demo-in-python-working-with-mobile-devices-5dce2bfc7b91">Part 4 : Working with Mobile Devices</a></li>
</ol>

This repo is the implementation of Part 4.
<br />
The original codes are <a href="https://github.com/ahmedfgad/FederatedLearning/tree/master/TutorialProject">here</a>.


## How to execute

```bash
python server/main.py
```

```bash
python server/client.py
```

1. Create, bind and starting listening on te server side.
2. Create, connect and start training on the client side.
