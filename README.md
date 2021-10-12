# DBIO Code Quality Moonshot initiative

<p align="left">
  <a href="https://github.com/intel-sandbox/frameworks.design.software.dbio.code-quality-moonshot/actions/workflows/ci.yaml?query=branch%3Amain">
    <img alt="Build" src="https://github.com/intel-sandbox/frameworks.design.software.dbio.code-quality-moonshot/actions/workflows/ci.yaml/badge.svg"></a>
</p>

## About

The DBIO Code Quality Moonshot is an initiative for defining a set of BKMs (Best Known Methods) for Code quality across DBIO.
 
The Objective is to help DBIO IOUs create code better, faster, with less bugs, by delivering an easy-to-use first step.

The Deliverable will be a template project, hosted on 1source, which may be used for forking new projects / aligning existing projects to those BKMs. The template will follow strict open source standards so it can be used for both public and private repos and include the following out of the box:
	
Dockerized build based on make with build, test and deploy targets
- Working CI using the dockerized make targets
- Automatic (language based) code formatting hooks
- Leading IDEs integrations
- Templates docs - `README.md`, `CONTRIBUTING.md` , `CODING_STYLE.md`.
- Issues & Pull Requests templates
- Versioning
- Recommended Workflows
  - Main branch broken
  - Release branch / tags
  - and more

The main branch will be without any code - it is the most generic template suited for all projects.
Other branches will be language specific - we will probably support Java, Python and C++ which are the main technologies used by Pensive Lake and Glade.
