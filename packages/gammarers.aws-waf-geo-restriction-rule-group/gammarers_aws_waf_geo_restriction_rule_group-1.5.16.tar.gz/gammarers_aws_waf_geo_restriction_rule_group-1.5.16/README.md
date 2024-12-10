# AWS WAF(v2) GEO Restriction Rule Group

[![GitHub](https://img.shields.io/github/license/gammarers/aws-waf-geo-restriction-rule-group?style=flat-square)](https://github.com/gammarers/aws-waf-geo-restriction-rule-group/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarers/aws-waf-geo-restriction-rule-group?style=flat-square)](https://www.npmjs.com/package/@gammarers/aws-waf-geo-restriction-rule-group)
[![PyPI](https://img.shields.io/pypi/v/gammarers.aws-waf-geo-restriction-rule-group?style=flat-square)](https://pypi.org/project/gammarers.aws-waf-geo-restriction-rule-group/)
[![Nuget](https://img.shields.io/nuget/v/Gammarers.CDK.AWS.WafGeoRestrictionRuleGroup?style=flat-square)](https://www.nuget.org/packages/Gammarers.CDK.AWS.WafGeoRestrictionRuleGroup/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/gammarers/aws-waf-geo-restriction-rule-group/release.yml?branch=main&label=release&style=flat-square)](https://github.com/gammarers/aws-waf-geo-restriction-rule-group/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gammarers/aws-waf-geo-restriction-rule-group?sort=semver&style=flat-square)](https://github.com/gammarers/aws-waf-geo-restriction-rule-group/releases)

[![View on Construct Hub](https://constructs.dev/badge?package=@gammarers/aws-waf-geo-restriction-rule-group)](https://constructs.dev/packages/@gammarers/aws-waf-geo-restriction-rule-group)

This is an AWS CDK Construct for Geo Restriction Rule Group on WAF V2

## Resources

This construct creating resource list.

* WAF V2 RuleGroup

## Install

### TypeScript

#### install by npm

```shell
npm install @gammarers/aws-waf-geo-restriction-rule-group
```

#### install by yarn

```shell
yarn add @gammarers/aws-waf-geo-restriction-rule-group
```

#### install by pnpm

```shell
pnpm add @gammarers/aws-waf-geo-restriction-rule-group
```

#### install by bun

```shell
bun add @gammarers/aws-waf-geo-restriction-rule-group
```

### Python

```shell
pip install gammarers.aws-waf-geo-restriction-rule-group
```

### C# / .Net

```shell
dotnet add package Gammarers.CDK.AWS.WafGeoRestrictionRuleGroup
```

## Example

```python
import { WafGeoRestrictRuleGroup } from '@gammarers/aws-waf-geo-restriction-rule-group';

new WafGeoRestrictRuleGroup(stack, 'WafGeoRestrictRuleGroup', {
  scope: Scope.GLOBAL, // GLOBAL(CloudFront) or REGIONAL(Application Load Balancer (ALB), Amazon API Gateway REST API, an AWS AppSync GraphQL API, or an Amazon Cognito user pool)
  allowCountries: ['JP'], // alpha-2 country and region codes from the International Organization for Standardization (ISO) 3166 standard
});
```

## License

This project is licensed under the Apache-2.0 License.
