---
date: 2026-11-19
slug: the-heat-exchanger-was-holding-back-on-purpose
categories:
  - House
  - Home Assistant
share: assets/social/the-heat-exchanger-was-holding-back-on-purpose.png
description: "The ventilation halved the radon. It also cost 640 watts, and one setting was the reason."
---

# The heat exchanger was holding back, on purpose

The ventilation halved the radon. It also cost 640 watts, and one setting was the reason.

<!-- more -->

The [last post about the ventilation](/balancing-ventilation-44-watts-for-200-m3h/) ended with the part I had not measured: the heat recovery. Winter will show, I wrote. It did, just not in the way I expected.

## Five years in one place

The Airthings in the living room has measured radon since November 2021, every five minutes. Home Assistant only had the last two weeks, so I exported the rest from Airthings' web page and loaded it into the ClickHouse database next to Home Assistant's own data. Next to it went hourly weather from two met.no stations a few kilometres away, and every hour of electricity since 2021 from Tibber.

That is almost two million rows. I did the digging with an AI agent that has read-only access to the database, which made it cheap to ask the next question.

<svg viewBox="0 0 680 192" role="img" aria-label="Radon in the living room, January to March average, Bq/m³. 2022: 111, 2023: 119, 2024: 113, 2025: 111, 2026: 57, the first winter with balanced ventilation." style="width:100%;max-width:680px;height:auto;font-family:inherit">
<text x="0" y="16" font-size="13" fill="currentColor" opacity="0.75">Radon in the living room, January to March, Bq/m³</text>
<text x="180" y="49" font-size="13" text-anchor="end" fill="currentColor">2022</text>
<rect x="190" y="34" width="351.5" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="549.5" y="49" font-size="13" fill="currentColor">111</text>
<text x="180" y="79" font-size="13" text-anchor="end" fill="currentColor">2023</text>
<rect x="190" y="64" width="376.8" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="574.8" y="79" font-size="13" fill="currentColor">119</text>
<text x="180" y="109" font-size="13" text-anchor="end" fill="currentColor">2024</text>
<rect x="190" y="94" width="357.8" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="555.8" y="109" font-size="13" fill="currentColor">113</text>
<text x="180" y="139" font-size="13" text-anchor="end" fill="currentColor">2025</text>
<rect x="190" y="124" width="351.5" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="549.5" y="139" font-size="13" fill="currentColor">111</text>
<text x="180" y="169" font-size="13" text-anchor="end" fill="currentColor">2026</text>
<rect x="190" y="154" width="180.5" height="20" rx="3" fill="#4f8cff"/>
<text x="378.5" y="169" font-size="13" fill="currentColor">57, with ventilation</text>
</svg>

The first winter with balanced ventilation has about half the radon of the four before it. The yearly average went from around 70 to 42 Bq/m³.

## Not a mild winter

A mild winter alone lowers radon, so I compared days with the same outdoor temperature.

<svg viewBox="0 0 680 268" role="img" aria-label="Radon by daily outdoor temperature, Bq/m³, before and after the ventilation: lower at every temperature, by about half on cold days." style="width:100%;max-width:680px;height:auto;font-family:inherit">
<text x="0" y="16" font-size="13" fill="currentColor" opacity="0.75">Radon by outdoor temperature that day, Bq/m³</text>
<text x="180" y="51" font-size="13" text-anchor="end" fill="currentColor">below −8 °C</text>
<rect x="190" y="34" width="293.1" height="13" rx="3" fill="currentColor" opacity="0.35"/>
<text x="489.1" y="45" font-size="11" fill="currentColor" opacity="0.8">81</text>
<rect x="190" y="49" width="173.7" height="13" rx="3" fill="#4f8cff"/>
<text x="369.7" y="60" font-size="11" fill="currentColor">48</text>
<text x="180" y="85" font-size="13" text-anchor="end" fill="currentColor">−8 to −3 °C</text>
<rect x="190" y="68" width="322.1" height="13" rx="3" fill="currentColor" opacity="0.35"/>
<text x="518.1" y="79" font-size="11" fill="currentColor" opacity="0.8">89</text>
<rect x="190" y="83" width="166.5" height="13" rx="3" fill="#4f8cff"/>
<text x="362.5" y="94" font-size="11" fill="currentColor">46</text>
<text x="180" y="119" font-size="13" text-anchor="end" fill="currentColor">−3 to 2 °C</text>
<rect x="190" y="102" width="347.4" height="13" rx="3" fill="currentColor" opacity="0.35"/>
<text x="543.4" y="113" font-size="11" fill="currentColor" opacity="0.8">96</text>
<rect x="190" y="117" width="231.6" height="13" rx="3" fill="#4f8cff"/>
<text x="427.6" y="128" font-size="11" fill="currentColor">64</text>
<text x="180" y="153" font-size="13" text-anchor="end" fill="currentColor">2 to 7 °C</text>
<rect x="190" y="136" width="358.3" height="13" rx="3" fill="currentColor" opacity="0.35"/>
<text x="554.3" y="147" font-size="11" fill="currentColor" opacity="0.8">99</text>
<rect x="190" y="151" width="206.3" height="13" rx="3" fill="#4f8cff"/>
<text x="402.3" y="162" font-size="11" fill="currentColor">57</text>
<text x="180" y="187" font-size="13" text-anchor="end" fill="currentColor">7 to 12 °C</text>
<rect x="190" y="170" width="264.2" height="13" rx="3" fill="currentColor" opacity="0.35"/>
<text x="460.2" y="181" font-size="11" fill="currentColor" opacity="0.8">73</text>
<rect x="190" y="185" width="213.5" height="13" rx="3" fill="#4f8cff"/>
<text x="409.5" y="196" font-size="11" fill="currentColor">59</text>
<text x="180" y="221" font-size="13" text-anchor="end" fill="currentColor">above 12 °C</text>
<rect x="190" y="204" width="126.7" height="13" rx="3" fill="currentColor" opacity="0.35"/>
<text x="322.7" y="215" font-size="11" fill="currentColor" opacity="0.8">35</text>
<rect x="190" y="219" width="94.1" height="13" rx="3" fill="#4f8cff"/>
<text x="290.1" y="230" font-size="11" fill="currentColor">26</text>
<rect x="190" y="246" width="12" height="12" rx="2" fill="currentColor" opacity="0.35"/><text x="208" y="257" font-size="12" fill="currentColor">Before (Nov 2021 to May 2025)</text>
<rect x="420" y="246" width="12" height="12" rx="2" fill="#4f8cff"/><text x="438" y="257" font-size="12" fill="currentColor">With ventilation</text>
</svg>

It is lower at every temperature, by about half on the cold days. January and February 2026 were cold, with weeks below −5 °C. Before the ventilation, windy days had a little more radon. Snow on the ground made no difference at all. The cause is mostly dilution: three hundred cubic metres an hour of fresh air.

## The bill

Then I did the same with the electricity. Per day, against the outdoor temperature, per heating season.

| Season | Power at 0 °C | Extra per degree colder |
|---|---:|---:|
| 2023/24 | 3.5 kW | 2.2 kWh/day |
| 2024/25 | 3.5 kW | 2.3 kWh/day |
| 2025/26, with ventilation | 4.3 kW | 3.1 kWh/day |

About 750 W more, at the same weather. Fresh air has to be heated, but the unit has a rotating heat exchanger rated up to 95%, and the electric reheater has been off for months. 750 W was too much.

## Sixteen degrees

The unit reports its temperatures to Home Assistant. Every day for two weeks the supply air was 15.5 °C, while the air from the rooms was 20 to 21 °C and the outside air around zero. The exchanger ran at 20 to 38% of its speed.

The reason was the supply set point, 16 °C. Below the set point the exchanger runs flat out. When the supply air reaches it, the unit slows the exchanger down, and the rest of the heat goes out with the exhaust. I had set it low to save the reheater. With the reheater off, a low set point saved nothing. It only threw heat away.

At 300 m³/h, 15.5 °C air into a 22 °C house is about 640 W of heat the floor heating and the heat pump have to make up for. Add the fans and you are at the 750 W.

The 84% on the dashboard was never wrong. That is what the exchanger can do. The set point decided how much of it the house got, and in practice it was about 75%.

| | Set point 16 °C | Set point 20.5 °C |
|---|---:|---:|
| Exchanger speed | 20–38% | 100% |
| Supply air | 15.5 °C | 19 °C |
| Exhaust air | 5–8 °C | 3 °C |
| Heat taken from the house | ~640 W | ~100 W |

My wife had said the living room felt cold all autumn. Air at 15.5 °C from the supply valves would do that.

## What it does now

Below 18 °C outside the set point is 20.5 °C, so every degree the exchanger can find stays in the house. Above 19 °C it drops to 16 °C, and the outside air goes past the exchanger and cools instead. The outside temperature is the median of four sensors around the house. The unit's own sensor reads about 3 °C too warm.

When CO2, radon, bathroom humidity and air pressure are all fine, the unit now also drops to its lowest mode, 200 m³/h. That is still above the requirement.

The duct sensors from last time do more now as well. Pressure in a duct goes with the square of the airflow, so with the balancing protocol as calibration they give airflow in m³/h. If it falls at the same fan speed, the filter is clogging. That is better than the unit's own filter warning, which is a six-month timer.

## What I got wrong

I took the set point at face value. It sounded like a comfort setting, and it was really the setting for how much heat to keep.

The sensor boxes also had their tubes on the wrong ports, which I found by turning on the cooker hood. It should give underpressure in the house, and the sensor said overpressure. While I stood there, I felt cold air pulled in around the attic hatch. That one goes both ways: most of the winter the top of the house is in slight overpressure, and then warm, moist air goes up into the cold attic instead. A strip of sealing tape will fix it.

The radon is still half of what it was. The heat bill for it is now about a sixth.
