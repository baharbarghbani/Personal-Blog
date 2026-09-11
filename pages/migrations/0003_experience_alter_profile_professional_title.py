from django.db import migrations, models


def populate_portfolio_from_cv(apps, schema_editor):
    """Populate the academic portfolio with public information from Bahar's CV."""

    Profile = apps.get_model("pages", "Profile")
    Research = apps.get_model("pages", "Research")
    Project = apps.get_model("pages", "Project")
    Experience = apps.get_model("pages", "Experience")

    profile = Profile.objects.order_by("pk").first()
    if profile:
        profile.full_name = "Bahar Barghbani"
        profile.professional_title = (
            "Computer Engineering · Computer Systems & Architecture"
        )
        profile.major = "B.Sc. in Computer Engineering"
        profile.institution = "Sharif University of Technology"
        profile.education_details = (
            "Expected graduation: July 2028\n"
            "Overall GPA: 18.58/20\n"
            "Major GPA: 18.89/20"
        )
        profile.location = "Tehran, Iran"
        profile.short_bio = (
            "Computer Engineering student interested in computer architecture, "
            "processor and memory systems, and reproducible performance research."
        )
        profile.about = (
            "I am a B.Sc. student in Computer Engineering at Sharif University of "
            "Technology, with an expected graduation date of July 2028. My overall "
            "GPA is 18.58/20 and my major GPA is 18.89/20.\n\n"
            "My current research focuses on computer architecture and performance "
            "evaluation. At Sabanci University, I develop reproducible C++ "
            "microbenchmarks and supporting infrastructure for studying compute, "
            "cache, and memory behavior. At the University of Murcia, I work on "
            "instruction prefetching and processor performance using gem5 and "
            "ChampSim.\n\n"
            "I also enjoy building systems-oriented projects, including MIPS "
            "processor implementations, a graph-neural-network approach to job-shop "
            "scheduling, a reconfigurable logic simulator, and a Git-like version "
            "control system written in C. Previously, I worked as a full-stack "
            "developer intern at Digikala.\n\n"
            "I ranked 441st among more than 136,000 participants in Iran's 2023 "
            "national university entrance exam and received a Bronze Medal in the "
            "2022 National Physics Olympiad. I have also served as a teaching "
            "assistant and contributed to student technical events. I speak Persian "
            "natively, use English professionally, and have intermediate Turkish and "
            "beginner French proficiency."
        )
        profile.research_interests = (
            "Computer Architecture\n"
            "Processor and Memory Systems\n"
            "Instruction Prefetching\n"
            "Performance Evaluation and Architectural Simulation\n"
            "Hardware-Software Co-Design\n"
            "Reproducible Systems Research"
        )
        profile.awards = (
            "Ranked 441st among 136,000+ participants in Iran's 2023 National "
            "University Entrance Exam (top 0.4%).\n"
            "Bronze Medal, 2022 National Physics Olympiad, selected from 9,000+ "
            "participants."
        )
        profile.technical_skills = (
            "Programming: C, C++, Python, Java\n"
            "Architecture and hardware: gem5, ChampSim, Verilog, MIPS Assembly, Logisim\n"
            "Systems and tooling: Linux, Git, CMake, Docker, GitHub Actions\n"
            "Web and databases: Django, React, Next.js, PostgreSQL, MySQL\n"
            "Technical communication: LaTeX, Markdown"
        )
        profile.languages = (
            "Persian: Native\n"
            "English: Professional proficiency\n"
            "Turkish: Intermediate\n"
            "French: Beginner"
        )
        profile.service = (
            "Sponsorship and executive roles for Codocodile and the Winter Seminar Series.\n"
            "Organizing contributions to ICPC 2023/24, Computer Engineering "
            "Introduction, and Rayan."
        )
        profile.email = "bahar.brqbni@gmail.com"
        profile.linkedin_url = "https://www.linkedin.com/in/baharbarghbani/"
        profile.github_url = "https://github.com/baharbarghbani"
        profile.save()

    Research.objects.update_or_create(
        slug="reproducible-processor-and-memory-system-characterization",
        defaults={
            "title": "Reproducible Processor and Memory-System Characterization",
            "field": "Computer Architecture and Memory Systems",
            "venue": "Sabanci University",
            "collaborators": "Supervisor: Prof. Özcan Öztürk",
            "year": 2026,
            "status": "ongoing",
            "summary": (
                "Reproducible microbenchmarking of compute, cache, and memory "
                "behavior for computer-systems research."
            ),
            "abstract": (
                "Developing focused C++ microbenchmarks and a reusable benchmark "
                "harness to characterize processor and memory-system behavior. The "
                "work includes controlled experiments, result analysis, and "
                "reproducible Linux-based research infrastructure using CMake, Git, "
                "and GitHub Actions."
            ),
            "featured": True,
            "is_visible": True,
            "display_order": 1,
        },
    )
    Research.objects.update_or_create(
        slug="instruction-prefetching-and-processor-performance",
        defaults={
            "title": "Instruction Prefetching and Processor Performance",
            "field": "Computer Architecture and Instruction Prefetching",
            "venue": "University of Murcia",
            "collaborators": "Supervisor: Prof. Alberto Ros",
            "year": 2026,
            "status": "ongoing",
            "summary": (
                "Evaluating instruction-prefetching techniques and processor "
                "performance with gem5 and ChampSim."
            ),
            "abstract": (
                "Building a reproducible gem5 baseline, investigating discrepancies "
                "between expected and observed results, and extending ChampSim for "
                "instruction-prefetching research. The project emphasizes careful "
                "simulation methodology and evidence-based performance analysis."
            ),
            "featured": True,
            "is_visible": True,
            "display_order": 2,
        },
    )

    Project.objects.update_or_create(
        slug="computer-architecture-course-project",
        defaults={
            "title": "Computer Architecture Course Project",
            "summary": (
                "Designed single-cycle, multi-cycle, and pipelined MIPS processors "
                "and evaluated cache behavior."
            ),
            "description": (
                "Implemented MIPS processor designs in Verilog and Logisim, including "
                "single-cycle, multi-cycle, and pipelined datapaths. Added a "
                "floating-point unit and used ChampSim to study cache and processor "
                "performance."
            ),
            "date_label": "June 2024",
            "technologies": "Verilog, Logisim, MIPS Assembly, ChampSim",
            "repository_url": (
                "https://github.com/baharbarghbani/Computer-Architecture"
            ),
            "featured": True,
            "is_visible": True,
            "display_order": 1,
        },
    )
    Project.objects.update_or_create(
        slug="job-shop-scheduling-with-graph-neural-networks",
        defaults={
            "title": "Job-Shop Scheduling with Graph Neural Networks",
            "summary": (
                "Applied graph neural networks and reinforcement learning to "
                "job-shop scheduling problems."
            ),
            "description": (
                "Represented scheduling instances as graphs, implemented a learning "
                "pipeline with PyTorch and DGL, and benchmarked learned policies "
                "against a randomized baseline across generated datasets."
            ),
            "date_label": "February 2026",
            "technologies": "Python, PyTorch, DGL, Reinforcement Learning",
            "repository_url": "https://github.com/radalj/Job-Scheduler",
            "featured": True,
            "is_visible": True,
            "display_order": 2,
        },
    )
    Project.objects.update_or_create(
        slug="reconfigurable-logic-simulator",
        defaults={
            "title": "Reconfigurable Logic Simulator",
            "summary": (
                "Built an interactive simulator for designing and testing digital "
                "logic circuits."
            ),
            "description": (
                "Created a visual logic-simulation environment in Python and PyGame "
                "and connected it to Arduino-based hardware for interactive circuit "
                "experiments."
            ),
            "date_label": "January 2025",
            "technologies": "Python, PyGame, Arduino, Digital Logic",
            "repository_url": (
                "https://github.com/baharbarghbani/reconfigurable-logic"
            ),
            "featured": False,
            "is_visible": True,
            "display_order": 3,
        },
    )
    Project.objects.update_or_create(
        slug="neogit",
        defaults={
            "title": "NeoGit",
            "summary": (
                "Implemented a compact Git-like version-control system in C."
            ),
            "description": (
                "Built core version-control concepts in C, including repository "
                "initialization, staging, commits, branch-oriented workflows, and "
                "history inspection."
            ),
            "date_label": "January 2024 - February 2024",
            "technologies": "C, Git, Command-Line Interfaces",
            "repository_url": "https://github.com/baharbarghbani/neogit-project",
            "featured": False,
            "is_visible": True,
            "display_order": 4,
        },
    )

    Experience.objects.update_or_create(
        role="Research Intern",
        organization="Sabanci University",
        defaults={
            "kind": "research",
            "location": "Istanbul, Türkiye",
            "date_label": "Summer 2026 - Present",
            "is_current": True,
            "summary": (
                "Developing reproducible C++ microbenchmarks and research "
                "infrastructure for processor and memory-system characterization "
                "under the supervision of Prof. Özcan Öztürk."
            ),
            "highlights": (
                "Build focused C++ microbenchmarks and a reusable benchmark harness.\n"
                "Study compute, cache, and memory behavior through controlled experiments.\n"
                "Maintain reproducible tooling with CMake, Git, GitHub Actions, and Linux."
            ),
            "featured": True,
            "is_visible": True,
            "display_order": 1,
        },
    )
    Experience.objects.update_or_create(
        role="Research Intern",
        organization="University of Murcia",
        defaults={
            "kind": "research",
            "location": "Remote",
            "date_label": "Summer 2026 - Present",
            "is_current": True,
            "summary": (
                "Researching instruction prefetching and processor performance with "
                "gem5 and ChampSim under the supervision of Prof. Alberto Ros."
            ),
            "highlights": (
                "Establish and validate a reproducible gem5 simulation baseline.\n"
                "Analyze discrepancies between expected and observed performance results.\n"
                "Extend ChampSim for instruction-prefetching experiments."
            ),
            "featured": True,
            "is_visible": True,
            "display_order": 2,
        },
    )
    Experience.objects.update_or_create(
        role="Full-Stack Developer Intern",
        organization="Digikala",
        defaults={
            "kind": "internship",
            "location": "Tehran, Iran",
            "date_label": "September 2024 - November 2024",
            "is_current": False,
            "summary": (
                "Built reusable interface components and improved page-loading "
                "behavior using React, Next.js, HTML, CSS, and Django."
            ),
            "featured": True,
            "is_visible": True,
            "display_order": 3,
        },
    )
    Experience.objects.update_or_create(
        role="Teaching Assistant",
        organization="Sharif University of Technology",
        defaults={
            "kind": "teaching",
            "location": "Tehran, Iran",
            "date_label": "Fall 2024 - Fall 2025",
            "is_current": False,
            "summary": (
                "Supported Fundamentals of Programming in C, Linear Algebra, and "
                "Probability and Statistics courses."
            ),
            "highlights": (
                "Fundamentals of Programming in C - Fall 2024.\n"
                "Linear Algebra - Spring and Fall 2025.\n"
                "Probability and Statistics - Fall 2025."
            ),
            "featured": False,
            "is_visible": True,
            "display_order": 4,
        },
    )


def reverse_portfolio_population(apps, schema_editor):
    """Preserve content if the schema migration is reversed."""


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0002_create_initial_profile"),
    ]

    operations = [
        migrations.CreateModel(
            name="Experience",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("role", models.CharField(max_length=180)),
                ("organization", models.CharField(max_length=180)),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("research", "Research"),
                            ("internship", "Internship"),
                            ("teaching", "Teaching"),
                            ("professional", "Professional"),
                        ],
                        max_length=20,
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=140)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                (
                    "date_label",
                    models.CharField(
                        blank=True,
                        help_text=(
                            "Optional display text such as 'Summer 2026 - Present'."
                        ),
                        max_length=100,
                    ),
                ),
                ("is_current", models.BooleanField(default=False)),
                (
                    "summary",
                    models.TextField(
                        help_text=(
                            "Briefly explain your responsibilities, contribution, and outcome."
                        )
                    ),
                ),
                (
                    "highlights",
                    models.TextField(
                        blank=True,
                        help_text="Enter one concrete accomplishment per line.",
                    ),
                ),
                ("organization_url", models.URLField(blank=True)),
                ("featured", models.BooleanField(default=False)),
                ("is_visible", models.BooleanField(default=True)),
                ("display_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": (
                    "display_order",
                    "-start_date",
                    "organization",
                    "role",
                ),
            },
        ),
        migrations.AddField(
            model_name="profile",
            name="awards",
            field=models.TextField(
                blank=True,
                help_text="Enter one honor or award per line.",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="education_details",
            field=models.TextField(
                blank=True,
                help_text=(
                    "Enter one education fact per line, such as graduation date or GPA."
                ),
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="languages",
            field=models.TextField(
                blank=True,
                help_text="Enter one language and proficiency level per line.",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="service",
            field=models.TextField(
                blank=True,
                help_text="Enter one service or student-leadership item per line.",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="technical_skills",
            field=models.TextField(
                blank=True,
                help_text="Enter one labeled skill group per line.",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="date_label",
            field=models.CharField(
                blank=True,
                help_text="Optional display text such as 'February 2026'.",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="professional_title",
            field=models.CharField(
                blank=True,
                default="Computer Engineering · Computer Systems & Architecture",
                max_length=180,
            ),
        ),
        migrations.RunPython(
            populate_portfolio_from_cv,
            reverse_portfolio_population,
        ),
    ]
