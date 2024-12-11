<!-- -*- mode: markdown; -*- -->

# theo-server

This is for a server which runs Theo, the order system.


## Updating Live Server

Note that this assumes you have defined `server` within your SSH config,
e.g. at `~/.ssh/config`.  Also you should configure the root password within
`./fabric.yaml`.

Install everything with:

    fab2 -e -H server bootstrap-all


## Testing with Vagrant

You should be able to get a VM going with a simple:

    vagrant up

You can then SSH directly into the VM with:

    vagrant ssh

You can confirm SSH credentials needed for connecting to it, with:

    vagrant ssh-config

Now you can "bootstrap" the machine with Fabric.  Please double-check your
`fabenv.py` file and make sure it contains:

    env.machine_is_live = False

After all this machine is *not* live, it's just for testing.  Finally, here is
the bootstrap command.  Note that it's possible you may need to modify some
parameters based on the output of `vagrant ssh-config` above.

    fab2 -e -H vagrant@localhost:2222 -i .vagrant/machines/default/virtualbox/private_key bootstrap-all
