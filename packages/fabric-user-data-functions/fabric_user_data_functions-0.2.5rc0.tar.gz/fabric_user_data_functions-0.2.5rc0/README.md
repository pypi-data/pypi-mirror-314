# Fabric Functions Python Worker

## Introduction

This project contains the necessary bindings and middleware we can register on a python function in order to receive fabric data from our worker extension. 

## Fabric Item Binding

By importing the `fabric_item_input` binding, the user can add a new attribute to their fabric function. This input has the same properties as the FabricItem attribute and binding from the host extension and will pass down to the worker the information to create a FabricItem: