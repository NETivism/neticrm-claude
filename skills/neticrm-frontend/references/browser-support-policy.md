# Browser Support Policy and CSS Technical Assessment Guide

This document integrates the company's browser support specifications and provides a complete guide for assessing the technical feasibility of CSS features.

---

## Company Browser Support Policy

### Basic Principles

**Definition of iOS/iPadOS Versions**

This specification adopts a rolling version support strategy, where **N** represents the latest major version officially released by Apple.

To confirm the latest version number (N), please refer to:
- [iOS version history - Wikipedia](https://en.wikipedia.org/wiki/IOS_version_history)
- Use WebSearch with the query: `"iOS version history" site:wikipedia.org`

### Support Scope

#### Desktop
- Supports the **Latest Stable Release** of major browsers: Chrome, Firefox, Edge, and Safari.
- **Does not support** any version of Internet Explorer (IE).

#### Tablets and Mobile Devices

**Android**
- Latest stable releases of Chrome and Firefox.

**iOS / iPadOS** (Uses an N-2 rolling support strategy)
- **Full Support**: The latest major version (N) and the previous major version (N-1).
- **Ensure Basic Browsing Only**: The major version before that (N-2).
- **End of Support**: All versions older than N-2 (Due to security concerns and technical limitations, users are encouraged to upgrade).

**Definition of "Ensure Basic Browsing Only"**
- ✅ Functional: Basic website layout, reading text content, and clicking links.
- ⚠️ May be unavailable: Dynamic effects, advanced interactive features, and certain visual styles.

---

## iOS Version Rolling Support Mechanism

Apple typically releases new iOS versions every September. The supported versions in this specification will automatically advance according to Apple's official release schedule.

### Rolling Update Illustration (Example: January 2026)

Due to Apple's unified version strategy adjustment in 2025, which jumped directly from iOS 18 to iOS 26, the support list will automatically adapt as follows:

- **Full Support**:
  - **Current Latest Version (N)**: iOS 26 / iPadOS 26
  - **Previous Version (N-1)**: iOS 18 / iPadOS 18 (*Note: Versions 19-25 were skipped*)
- **Basic Browsing**: **Version before that (N-2)**: iOS 17 / iPadOS 17
- **End of Support**: iOS 16 / iPadOS 16 and below.

**Important Reminder**: After Apple releases a new version every September, the support list will be updated automatically. When evaluating CSS technology, always confirm the current value of N first. To confirm the latest version number (N), refer to:
- [iOS version history - Wikipedia](https://en.wikipedia.org/wiki/IOS_version_history)
- Use WebSearch with the query: `"iOS version history" site:wikipedia.org`

---

## iOS Browser Limitation Description

### Technical Limitations

Due to Apple's App Store policies, all third-party browsers on iOS (including Chrome and Firefox) are **forced to use the WebKit engine**.

Specific limitations include:
1. Chrome cannot use its native Blink engine, and Firefox cannot use its Gecko engine.
2. JavaScript performance is restricted because they cannot use their own JavaScript engines.
3. Certain web features may not function as expected because they must follow WebKit's implementation.

### EU Exception (iOS 17.4+)
- Non-WebKit engines can only be used within the European Economic Area (EEA).
- Must comply with Apple's security specifications, review requirements, and commercial agreements.

### Technical Impact

**JavaScript Limitations**
- JavaScript engine performance depends on WebKit.
- Some web features may not be fully supported.

**CSS Limitations**
- CSS support across all browsers on iOS is identical to iOS Safari (WebKit).
- Support for new features depends on the WebKit implementation timeline.
- **When evaluating CSS technology, you only need to check the support status for iOS Safari.**

---

## CSS Technical Feasibility Assessment Process

### ⚠️ Mandatory Rule: Real-time Lookup Required

**CRITICAL - MUST COMPLY**:

When evaluating the browser support of any CSS technology, it is **strictly prohibited** to judge based solely on Claude's knowledge cutoff date (January 2025).

**You MUST perform a WebSearch or WebFetch to check for the latest browser support information** before giving a conclusion.

**Situations where a lookup is mandatory**:
- Any CSS technology that appears "new," "experimental," or "uncommon."
- Any technique using `::` pseudo-elements or `@` rules (except basic @media).
- Technologies containing keywords like `scroll-`, `container-`, `@layer`, `@property`, etc.
- When a user explicitly requests a browser support evaluation.
- When the support status for a technology is "uncertain" or "unclear."

**Exceptions for lookups**: Limited to very mature foundational technologies (Flexbox, CSS Grid, CSS Variables, transition, animation).

---

### Core Concept: Core Functionality vs. Enhancement Effects

**Core Functionality** (Affects the main layout or content display of the website)
- Must be supported down to the "Ensure Basic Browsing Only" version (N-2).
- Recommended to reach the [Baseline Widely available](https://developer.mozilla.org/en-US/docs/Glossary/Baseline/Compatibility#baseline_badges) standard.
- Examples: CSS Grid, Flexbox, basic selectors.

**Enhancement Effects** (Decorative features that improve the experience)
- Only need to support the "Full Support" versions (N and N-1).
- Recommended to reach the [Baseline Newly available](https://developer.mozilla.org/en-US/docs/Glossary/Baseline/Compatibility#baseline_badges) standard.
- Examples: Scroll-driven Animations, text-autospace.

### Assessment Steps

**Step 0: Check if a lookup is needed (Execution Mandatory)**

Before performing any evaluation, determine if a lookup is required:
- Does this CSS technology fall into the "Mandatory Lookup" range? (See mandatory rules above)
- If yes, **perform the lookup immediately**; do not skip it.

**Step 1: Confirm Current Support Policy**

Use WebSearch to find the latest iOS version:
```
Example query:
"iOS version history" site:wikipedia.org
"latest iOS version 2026"
```

Confirm current values for N, N-1, and N-2 (e.g., 26, 18, 17 in Jan 2026).

**Step 2: Technical Support Check (Mandatory)**

**Must actually perform a lookup** on [MDN](https://developer.mozilla.org/) or [caniuse.com](https://caniuse.com/) to confirm the status of the technology:

Using WebFetch:
```
URL: https://caniuse.com/?search=[CSS_Technology_Name]
Prompt: "Extract browser support information for this CSS technology, specifically the minimum support version for iOS Safari and its Baseline status."
```

Or using WebSearch:
```
Example queries:
"[CSS_Technology_Name] caniuse 2026"
"[CSS_Technology_Name] browser support iOS Safari"
"[CSS_Technology_Name] MDN baseline"
```

**Important**: You must wait for the lookup results before proceeding; do not judge based on outdated knowledge.

**Step 3: Determine Technology Type**

- Is this technology "Core Functionality" or an "Enhancement Effect"?
- Core Functionality: Lack of support results in a broken layout or invisible content.
- Enhancement Effect: Lack of support only results in missing extra effects without affecting basic reading.

**Step 4: Consult the Decision Tree**

Make a decision based on technology type and support status (see the Decision Tree below).

---

## Decision Tree

```
Need to use a certain CSS technology?
│
├─ Step 1: Confirm current support policy (N, N-1, N-2)
│  └─ Lookup iOS version history
│
├─ Step 2: Check technical support
│  ├─ Lookup caniuse.com / MDN
│  └─ Confirm minimum iOS Safari support version
│
├─ Step 3: Determine technology type
│  ├─ Core Functionality?
│  │  ├─ Min iOS support version <= N-2?
│  │  │  ├─ Yes → ✅ Can be used directly
│  │  │  └─ No → ❌ Not recommended; wait for better support or use a fallback
│  │  └─ Reaches Baseline Widely available?
│  │     ├─ Yes → ✅ Preferred use
│  │     └─ No → ⚠️ Use with caution; provide a fallback
│  │
│  └─ Enhancement Effect?
│     ├─ Min iOS support version <= N-1?
│     │  ├─ Yes → ✅ Can be used (Progressive Enhancement)
│     │  └─ No → ⚠️ Only use for N version; let it degrade naturally on older versions
│     └─ Reaches Baseline Newly available?
│        ├─ Yes → ✅ Can be used
│        └─ No → ⚠️ Experimental; use with caution
```

---

## Practical Assessment Cases

### Case 1: CSS Grid

**Lookup Results** (Example)
- Baseline Status: Widely available
- Min iOS Safari Version: iOS 10.3+

**Assessment Result** (As of Jan 2026)
- Company Support Scope: Full support 26, 18; Basic browsing 17
- Tech Type: **Core Functionality** (Affects layout)
- **Conclusion**: ✅ Can be used directly without a fallback.
- **Reason**: Support has reached Baseline Widely available, and the supported version is far below the company's minimum support version.

### Case 2: CSS Nesting

**Lookup Results** (Example)
- Baseline Status: 2023 Newly available
- Min iOS Safari Version: iOS 16.5 (Partial) / iOS 17.2 (Full)

**Assessment Result** (As of Jan 2026)
- Company Support Scope: Full support 26, 18; Basic browsing 17
- Tech Type: **Core Functionality** (Affects CSS architecture handling)
- **Conclusion**: ❌ Not recommended for direct use (use transpilation if necessary).
- **Reason**:
  - Has not reached the Baseline Widely available standard.
  - Although the "Basic Browsing" version has advanced to iOS 17, iOS 17.0 - 17.1 only offers partial support (e.g., it doesn't support Type Selectors in nesting). Using native syntax directly might break the layout on iOS 17.0/17.1 devices, failing the "Ensure Basic Browsing" requirement.
- **Recommendation**:
  - Stick to traditional CSS syntax until the technology is compatible with the minimum version in the company's support policy.
  - If you need to use it, do so locally and transpile to traditional CSS using SCSS/SASS for deployment.

### Case 3: CSS text-autospace

**Lookup Results** (Example)
- Baseline Status: 2025 Newly available
- Min iOS Safari Version: iOS 18.4+

**Assessment Result** (As of Jan 2026)
- Company Support Scope: Full support 26, 18; Basic browsing 17
- Tech Type: **Enhancement Effect** (Improves reading experience, non-essential)
- **Conclusion**: ✅ Recommended for direct use (as Progressive Enhancement).
- **Reason**:
  - **Enhancement Effect**: This property improves the reading experience (spacing between Chinese/English characters). If the browser doesn't support it, the text is still readable; it just lacks extra spacing and doesn't affect functionality, meeting the "Basic Browsing" definition.
  - **Advantage over alternatives**: Compared to traditional JavaScript solutions (like `pangu.js`), native CSS offers better performance and avoids layout shifts caused by loading delays.
- **Recommendation**:
  - Set `text-autospace: normal` to enable default automatic spacing.
  - No need to create polyfills for older browsers; let them undergo graceful degradation.

### Case 4: WebP Image Format

**Lookup Results** (Example)
- Baseline Status: Widely available
- Min iOS Safari Version: iOS 14.0+

**Assessment Result** (As of Jan 2026)
- Company Support Scope: Full support 26, 18; Basic browsing 17
- Tech Type: **Core Functionality** (Affects content display)
- **Conclusion**: ✅ Can be used directly.
- **Reason**:
  - **Maturity**: It has reached Baseline Widely available, and support (iOS 14) is well below the current minimum of iOS 17.
- **Recommendation**:
  - WebP can be used as the default image format for the project without needing fallbacks, unless there are extremely specific legacy system requirements.

### Case 5: CSS `:has()` Selector

**Lookup Results** (Example)
- Baseline Status: 2023 Newly available
- Min iOS Safari Version: iOS 15.4+

**Assessment Result** (As of Jan 2026)
- Company Support Scope: Full support 26, 18; Basic browsing 17
- Tech Type: **Core Functionality** (Affects layout structure control)
- **Conclusion**: ✅ Can be used directly.
- **Reason**:
  - Although "Newly available," its minimum support version (iOS 15.4) fully covers the iOS 17 required by the "Basic Browsing" definition.
- **Recommendation**:
  - Can fully replace older methods that required toggling classes via JavaScript to control parent styles, improving development efficiency and performance.

### Case 6: Scroll-driven Animations

**Lookup Results** (Example)
- Baseline Status: Has not reached stable Baseline support (WebKit still in experimental phase or new version integration).
- Min iOS Safari Version: iOS 18+ (Expected)

**Assessment Result** (As of Jan 2026)
- Company Support Scope: Full support 26, 18; Basic browsing 17
- Tech Type: **Enhancement Effect** (Visual animation, non-essential)
- **Conclusion**: ✅ Recommended as Progressive Enhancement.
- **Reason**:
  - **Enhancement Effect**: Scroll animations are decorative. If unsupported, users can still read content and interact with links normally, meeting the "Basic Browsing" definition.
  - **Version Limitation**: This technology does not work on iOS 17 (N-2), failing the core functionality principle of supporting down to N-2.
- **Recommendation**:
  - Provide smooth native CSS animations for supported devices.
  - Let it degrade naturally on older devices like iOS 17; do not load extra polyfills just to achieve the animation effect.

---

## Quick Checklist

Before using a new CSS technology, please confirm:

- [ ] Checked current iOS support policy (N, N-1, N-2).
- [ ] Checked support status on caniuse.com or MDN.
- [ ] Confirmed minimum iOS Safari support version.
- [ ] Determined if it is "Core Functionality" or an "Enhancement Effect."
- [ ] Core Functionality: Confirmed min support version <= N-2.
- [ ] Enhancement Effect: Confirmed it can degrade naturally on older versions without affecting basic browsing.
- [ ] Prepared a fallback or transpilation tool if using a new technology with insufficient support.

---

## References

- **iOS Version History**: https://en.wikipedia.org/wiki/IOS_version_history
- **Can I Use**: https://caniuse.com/ - Browser support lookups
- **MDN Web Docs**: https://developer.mozilla.org/ - Complete documentation and Baseline markers
- **Baseline**: https://web.dev/baseline/ - Explanation of cross-browser support status
