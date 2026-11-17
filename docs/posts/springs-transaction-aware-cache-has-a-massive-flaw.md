---
date: 2019-08-05
categories:
  - Java
  - Spring
---

# Spring's transaction-aware cache has a massive flaw

Spring has a decorator that keeps your cache honest when a transaction rolls back. It does that by lying to you until the transaction is over.

<!-- more -->

The idea is sound. If you write to a cache inside a transaction and the transaction rolls back, the cache holds a value that never existed in the database. So `TransactionAwareCacheDecorator` holds the write back until commit.

The problem is that it holds it back from you as well.

```java
cache.put("foo", "bar");
cache.get("foo");   // null, until the transaction has committed
```

That one you notice. The other case is worse. The key already had a value, you update it, and every read for the rest of the transaction gives you the old one. There is no error and nothing in the log. Writing data and then reading it back gives you what was there before you wrote. I cannot think of a case where anyone wants that.

<svg viewBox="0 0 680 142" role="img" aria-label="Timeline of put, get, commit and get. Spring returns the old value before commit, the replacement returns the new one." style="width:100%;max-width:680px;height:auto;font-family:inherit">
<text x="0" y="16" font-size="13" text-anchor="start" fill="currentColor" opacity="0.75">One transaction, with the key already cached as “old”.</text>
<line x1="20" y1="70" x2="660" y2="70" stroke="currentColor" stroke-opacity="0.5"/>
<rect x="20" y="64" width="420" height="12" rx="3" fill="currentColor" opacity="0.15"/>
<circle cx="60" cy="70" r="5" fill="currentColor"/>
<text x="60" y="50" font-size="13" text-anchor="middle" fill="currentColor" font-family="monospace">put(k, new)</text>
<circle cx="250" cy="70" r="5" fill="currentColor"/>
<text x="250" y="50" font-size="13" text-anchor="middle" fill="currentColor" font-family="monospace">get(k)</text>
<circle cx="440" cy="70" r="5" fill="currentColor"/>
<text x="440" y="50" font-size="13" text-anchor="middle" fill="currentColor" font-family="monospace">commit</text>
<circle cx="620" cy="70" r="5" fill="currentColor"/>
<text x="620" y="50" font-size="13" text-anchor="middle" fill="currentColor" font-family="monospace">get(k)</text>
<text x="20" y="104" font-size="12" text-anchor="start" fill="currentColor" opacity="0.6">Spring</text>
<text x="20" y="130" font-size="12" text-anchor="start" fill="currentColor" opacity="0.6">Mine</text>
<text x="250" y="104" font-size="14" text-anchor="middle" fill="currentColor" font-weight="600">old</text>
<text x="620" y="104" font-size="14" text-anchor="middle" fill="currentColor">new</text>
<text x="250" y="130" font-size="14" text-anchor="middle" fill="#4f8cff" font-weight="600">new</text>
<text x="620" y="130" font-size="14" text-anchor="middle" fill="#4f8cff">new</text>
</svg>

So you turn on the safe option, and your code starts acting on stale data. Or it misses the cache every time and goes to the database, and the cache you added for speed does nothing in the place where you do most of the work.

The name says transaction aware, and I took that to mean what I wanted it to mean.

## What I did instead

[spring-tx-cache-decorator](https://github.com/ethlo/spring-tx-cache-decorator) keeps a transient cache for the length of the transaction. Reads look there first, then in the real cache. On commit the transient values are merged into the real cache. On rollback they are thrown away. The same goes for `evict` and `clear`: you see your own changes, and nobody else does until commit.

```java
final Cache myCache = myCacheManager.getCache("my-cache");
final Cache wrapped = new EnhancedTransactionAwareCacheDecorator(myCache, cacheCacheResult);
```

This is the rollback test:

```java
@Test
public void testInvokePutInsideTransactionWithRollback()
{
    mockTxnManager(true);
    decoratorA.put("foo", "bar");

    // Make sure the transient cache holds this
    assertThat(decoratorA.get("foo", String.class)).isEqualTo("bar");

    // Should not yet be in the cache itself
    assertThat(realCacheA).doesNotContainKeys("foo");

    // Rollback
    mockTransactionEnd(false);

    // Make sure the cache does not hold it
    assertThat(decoratorA.get("foo", String.class)).isNull();
}
```

Knowing where the transaction starts and ends gave me one more thing. A value read from a remote cache can be kept in the transient one, so the second read in the same transaction costs a map lookup and no round trip. That is the `cacheCacheResult` flag. It is off by default, since it only helps when the same key is read more than once.

## It is not a transactional cache

I should be careful here, since I just complained about a name that promises too much. This does not make your cache transactional. It only stops the real cache from being filled before commit. Isolation is roughly read committed: when another transaction commits a change, you see it at once. There is no locking, and two transactions that write the same key both win, in commit order.

## Why not fix it in Spring?

It has been reported, as [issue 17353](https://github.com/spring-projects/spring-framework/issues/17353). I assume the behaviour is kept for compatibility. A decorator of my own was quicker than waiting.

It still surprises me that this is the default.
