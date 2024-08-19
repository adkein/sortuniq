sortuniq
====

Motivating use case
----

Suppose you have a long stream of input. For example, you can stream the length of each filename
that your user has permission to read:

```
find / 2>/dev/null | awk '{print length($0)}'
```

Suppose we want the distribution of these filename lengths, for whatever reason. Then with existing
tools we could do this:

```
find / 2>/dev/null | awk '{print length($0)}' | sort | uniq -c
```

What `sortuniq` does is the same thing but `sortuniq` also displays periodically the intermediate
running counts, so you are no longer left hanging in suspense:

```
find / 2>/dev/null | awk '{print length($0)}' | sortuniq
```

Usage
----

In the example in the previous section, `sortuniq` is executed without any options. By default the
update interval is 1 second. You can specify the update interval with the `-t` option, e.g. `-t 3`
for a 3-second interval. You can specify that the updates occur after every `N` lines of input
(instead of at intervals of time) by passing `-s N`.

For full usage details:

```
sortuniq -h
```

Installation
----

Clone this repository and:

```
cd sortuniq
sudo pip3 install -r requirements.txt
sudo python3 setup.py install
```
