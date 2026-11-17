---
date: 2025-09-19
categories:
  - Java
  - Spring
  - Performance
---

# 5,800 to 53,000 req/s by skipping the filter chain

I made a Spring endpoint nine times faster this week. The way I did it is by skipping most of what Spring does to keep you safe.

<!-- more -->

A minimal echo endpoint on the standard Spring MVC path gave 5,800 requests per second. The same endpoint on my fast path gave 53,000. The numbers are from a real application with several hundred mappings, not from a hello world project.

<svg viewBox="0 0 680 98" role="img" aria-label="Echo endpoint, requests per second. Higher is better." style="width:100%;max-width:680px;height:auto;font-family:inherit">
<text x="0" y="16" font-size="13" text-anchor="start" fill="currentColor" opacity="0.75">Echo endpoint, requests per second. Higher is better.</text>
<text x="180" y="49" font-size="13" text-anchor="end" fill="currentColor">Standard Spring MVC</text>
<rect x="190" y="34" width="41.6" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="239.6" y="49" font-size="13" text-anchor="start" fill="currentColor">5,800</text>
<text x="180" y="79" font-size="13" text-anchor="end" fill="currentColor">Fast path</text>
<rect x="190" y="64" width="380.0" height="20" rx="3" fill="#4f8cff"/>
<text x="578.0" y="79" font-size="13" text-anchor="start" fill="currentColor">53,000</text>
</svg>

So for a simple endpoint, about nine tenths of the request is spent before your code runs. The request goes through every servlet filter, the security filter chain parses the same path again for each pattern it holds, and then the `DispatcherServlet` finds the handler. With hundreds of mappings and a long list of security patterns, that work is far larger than an echo.

## What the library does

[spring-mvc-fastpath](https://github.com/ethlo/spring-mvc-fastpath) is a Spring Boot starter. You mark the hot endpoints:

```java
@MvcAccelerator
@GetMapping("/echo")
public String echo(@RequestParam String value)
{
    return value;
}
```

Requests to those take a short route past the `DispatcherServlet`, and run only the filters you list:

```yaml
mvc:
  accelerator:
    fast-filter-chain:
      mode: ANNOTATED
      fail-if-filter-missing: true
      included-filters:
        - com.example.filters.MyCustomLoggingFilter
```

There is also a request matcher that caches the parsed path for the length of one request, so the security chain does not parse it again for every pattern. That one is safe to use by itself.

## A shortcut around security

I am normally the one who says no to shortcuts around security. This library is a shortcut around security, and the first thing in its README is a warning.

A filter you did not list does not run. If that filter was the one doing authentication, the endpoint is open, and nothing will tell you. That is why `fail-if-filter-missing` is on by default, so a typo in a class name stops the application at startup. It does not help if you forget the filter altogether.

For most endpoints it is not worth it. Once the handler does a database call, the framework overhead is a small part of the request and the gain goes away. It pays off for the few endpoints that are hit all the time and do almost nothing.

It is not in production with us. I am not sure it should be.
