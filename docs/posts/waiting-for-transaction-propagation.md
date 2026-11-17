---
date: 2016-01-05
categories:
  - Archive
share: assets/social/waiting-for-transaction-propagation.png
description: "In the land of traditional ACID DBs, I often encounter code that is trying to collaborate with some external system using a queue or notification system. The problem is that it ends up sending the…"
---

# Waiting for transaction propagation

In the land of traditional ACID DBs, I often encounter code that is trying to collaborate with some external system using a queue or notification system. The problem is that it ends up sending the notification to the external system before the data has been committed to the central database. Then when the external system tries to query for data based on the notification, the data is not there yet (a different or outside a transaction).

<!-- more -->

The remedy I see most often is using a delay using `Thread.sleep()`.

Why is this a problem? First of all you have no idea how long you may need to sleep, as it is affected by the transaction and data size and the amount of load on the database, so you will have to wait a long time just to be *almost* sure. The other problem you have now introduced is that *all* processes are now delayed for at least the amount of time the process waits.

This is probably known to many people already (but obviously not everyone), so here goes:

```java
private SomeNotificationService delegate;

public void process(final Object event)
{
  TransactionSynchronizationManager.registerSynchronization(
    new TransactionSynchronizationAdapter()
    {
      @Override
      public void afterCommit()
      {
        delegate.sendEvent(event);
      }
    });
}
```

That’s it! Spring’s transaction handling will wait until the transaction is finished until it sends the notification (or not at all if the commit fails).

Simple, yet very powerful!
