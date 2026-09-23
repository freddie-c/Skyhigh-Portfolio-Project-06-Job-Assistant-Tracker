# Role Research — Junior/Mid DevOps & Infrastructure Engineer

## Target role and title aliases

Target: **DevOps / Infrastructure Engineer** at the junior-to-mid level, AWS-focused.

I am not targeting a single job title. At first I searched for "DevOps Engineer" and
got almost nothing back from the boards I could legally pull from. The same work shows
up under a lot of different names depending on the company, so the role is defined as
a title family plus a skill set:

- DevOps Engineer
- Infrastructure Engineer
- Platform Engineer
- Cloud Engineer
- Site Reliability Engineer
- Software Engineer, Infrastructure / Site Reliability

This alias list is configuration, and not code. It lives on the role-specific side of the
project so anyone targeting a different role can swap it out without touching the
aggregation logic.

## Evidence postings (pulled 2026-09-21)

| # | Company | Title | Level signal | Link |
|---|---------|-------|--------------|------|
| 1 | Upstart | DevOps Engineer II, Cloud Platform | 3+ yrs, bachelor's or equivalent | https://careers.upstart.com/jobs?gh_jid=8030908 |
| 2 | Upstart | Software Engineer, Site Reliability | 3+ yrs, on-call experience expected | https://careers.upstart.com/jobs?gh_jid=8223417 |
| 3 | P\S\L Group | Senior DevOps Engineer | 5–7 yrs total, 3–5 in AWS; Malaysia-based | https://job-boards.greenhouse.io/pslgroup/jobs/6187827004 |

Posting #3 is out of reach for me and truly not in consideration as a position I would accept. It is senior and in the wrong region. I kept it because it is a useful market signal for which tools keep showing up, and I want the keyword counts to reflect the market rather than only the two roles I would actually accept.

## In-demand tools and keywords

Counted across the three postings above. "Required" means it appeared in minimum
qualifications; "preferred" means bonus or nice-to-have; "responsibility" means it
showed up in the day-to-day work section instead of the requirements list.

| Keyword | Upstart DevOps II | Upstart SRE | P\S\L Senior | Count |
|---|---|---|---|---|
| AWS | required | preferred | required | 3/3 |
| Infrastructure as Code (Terraform) | required | preferred | required | 3/3 |
| Observability / monitoring / logging | responsibility | required | responsibility | 3/3 |
| Incident response / on-call | required | required | responsibility | 3/3 |
| SLOs and reliability practices | required | preferred | responsibility | 3/3 |
| Kubernetes | required | preferred | — | 2/3 |
| CI/CD and GitOps | required | — | required | 2/3 |
| CloudFormation / CDK / Ansible | CDK | — | both | 2/3 |
| AI-assisted development tooling | — | required | required | 2/3 |
| Python or Go | — | required | — | 1/3 |
| ArgoCD | required | — | — | 1/3 |
| Service mesh (Istio / Envoy) | preferred | — | — | 1/3 |

Notes on the counts:

- The five 3/3 keywords are the true indicator. AWS, IaC, observability, incident response,
  and SLOs showed up in every posting regardless of title or level.
- Kubernetes reads as 2/3 only because P\S\L does not use it. Both Upstart roles want
  it and one lists it as a hard requirement, so I am treating it as core.
- AI-assisted tooling at 2/3 was somewhat surprising to me. Both the SRE role and the P\S\L role ask
  for it directly, and P\S\L goes further and wants prompt and agent-skill authoring.
  That is new enough that I am flagging it rather than weighting it like the others.

## What a strong resume looks like

**There is no junior tier on these boards.** Every posting I found asks for 3+ years,
and the senior one asks for 5–7. Nothing I swept was entry level. A resume that gets
a callback here has to show production-shaped work, not coursework. So my projects
need to read like systems I operated, not tutorials I finished.

**The title tells you almost nothing.** Upstart's reliability role is titled "Software
Engineer, Site Reliability" and wants Kubernetes, AWS, IaC, and observability. Stripe
titles the same kind of work "Software Engineer, Core Infrastructure." Filtering on
the word "DevOps" would have hidden both. The requirements block is the real signal,
and my tool has to read it.

**Where I match:** AWS, Terraform, CI/CD, Kubernetes, and Prometheus/Grafana are all
things I have built and can talk through end to end.

**Where I am short:** Incident response and SLOs. Every posting wants on-call
experience, post-incident reviews, and service level objectives. I have built a
monitoring stack, but "I built alerting" is not the same claim as "I have been paged
and ran the incident." I need to either get that experience or frame my monitoring
work in reliability terms — error budgets, failure modes, recovery — instead of tool
terms.

**What gets filtered:** Generic cloud language with no system attached. "Familiar with
AWS" says nothing. "Built a VPC with public and private subnets across two AZs in
Terraform" is the same claim with evidence.

## Target profile

I am a junior-to-mid DevOps and Infrastructure Engineer targeting AWS-focused platform
roles. My strongest, most defensible work is infrastructure as code with Terraform,
containerized services on Kubernetes, CI/CD pipelines in GitHub Actions that build,
test, and deploy to a cluster, and a production-style monitoring stack built on
Prometheus and Grafana with alerting. Bullets tailored for me should lead with the
system I built and what it did in production terms — what it deployed, what it
monitored, what failure it caught — not with the tool name. Reliability framing
(SLOs, failure modes, recovery, reducing manual toil) should be preferred over feature
framing wherever the evidence supports it. Do not claim on-call or incident response
experience; that is a real gap and should be surfaced in the keyword-gap summary
instead of written into a bullet.

## Method notes

I expected DevOps and Platform titles to dominate on Greenhouse boards. I was wrong,
and the data corrected me a few times.

**First sweep — Stripe only.** Grepping titles for `devops|platform|cloud|infra`
returned mostly Account Executives, because "Platforms" at Stripe is a sales
territory. Zero DevOps titles. My grep was a naive classifier and I watched it produce
mostly false positives.

**Second sweep — four boards.** Stripe, Databricks, GitLab, and Vercel: still zero
DevOps titles across all four. Infra work at engineering-led companies is titled
"Software Engineer, Infrastructure." Almost everything left was senior or staff. I had
picked those four companies because I knew they used Greenhouse, not because they hire
juniors, so the sample was biased by my own selection.

**Third pass — targeted search.** I used `site:job-boards.greenhouse.io "devops
engineer"` to find boards that actually use the title, which got me Upstart and
P\S\L Group. Upstart turned out to be the richest board, with both a leveled DevOps
role and an unleveled SRE role.

**The funnel:** 54 raw title matches → 10 after excluding senior and non-engineering
rows → 3 selected after reading requirements.

**The denylist problem.** Every exclusion I added revealed the next one. I cut
`manager|staff|principal|director|senior`, and then "Sr Software Engineer" got through
because my pattern only matched "Sr." with a period. I fixed that and "Strategic Cloud
Partnerships Lead" got through. A denylist that keeps growing is a design smell, and
it is the main reason Ticket 1 needs to match on the description instead of the title
alone.

**Ensono.** I found a relevant DevOps posting at Ensono, but it lives on their own
careers site rather than a Greenhouse board, so the API sweep cannot reach it. That is
not a dead end. Ticket 1 requires a careers page or RSS feed as a second source type,
and Ensono is a candidate for exactly that.