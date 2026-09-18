<h2><a href="https://leetcode.com/problems/encode-and-decode-strings">Encode and Decode Strings</a></h2> <img src='https://img.shields.io/badge/Difficulty-Medium-orange' alt='Difficulty: Medium' /><hr><p><em>LeetCode Premium. Solved on neetcode.io, where the same problem is free, so there is no accepted submission for <code>leetcode_pull.py</code> to find and this directory was written by hand. A future re-solve will need a manual commit too, or the review ladder will not advance.</em></p>

<p>Design an algorithm to encode a list of strings to a single string. The encoded string is then decoded back to the original list of strings.</p>

<p>Please implement <code>encode</code> and <code>decode</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">["neet","code","love","you"]</span></p>

<p><strong>Output:</strong> <span class="example-io">["neet","code","love","you"]</span></p>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">["we","say",":","yes"]</span></p>

<p><strong>Output:</strong> <span class="example-io">["we","say",":","yes"]</span></p>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>0 &lt;= strs.length &lt; 100</code></li>
	<li><code>0 &lt;= strs[i].length &lt; 200</code></li>
	<li><code>strs[i]</code> contains only UTF-8 characters.</li>
</ul>

<p>&nbsp;</p>
<p><strong>Note:</strong> the string may contain any character, including the delimiter you pick and text that looks like your own encoding &mdash; <code>["3#x", "0#", "##"]</code> is a legal input.</p>
