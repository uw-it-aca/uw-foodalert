# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from django_dbq.models import Job
from django_dbq.management.commands.worker import process_job
from django_dbq.management.commands.worker import DEFAULT_QUEUE_NAME


class Command(BaseCommand):
    help = 'Processes (a max of n) jobs from the front of the queue'

    def add_arguments(self, parser):
        parser.add_argument('n_jobs',
                            nargs='?',
                            type=int,
                            help='Max number of jobs to process',
                            default=3)

    def handle(self, *args, **options):
        n_jobs = options['n_jobs']
        jobs_in_queue = self.jobs_in_queue()
        if (jobs_in_queue == 0):
            self.stdout.write(
              'There are no jobs in the queue'
            )
        else:
            self.stdout.write(
              'Starting job worker for queue "%s"'
              % (DEFAULT_QUEUE_NAME)
            )
            jobs_processed = 0
            while jobs_in_queue > 0 and jobs_processed <= n_jobs:
                process_job(DEFAULT_QUEUE_NAME)
                jobs_in_queue = self.jobs_in_queue()
                jobs_processed += 1

            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully processed %s jobs'
                    % jobs_processed
                )
            )

    def jobs_in_queue(self):
        return Job.objects.exclude(state=Job.STATES.COMPLETE).count()
