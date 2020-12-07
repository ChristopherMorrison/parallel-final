from celery import shared_task


@shared_task
def evaluate_vuln_by_model(binary_files):
    """Given a list of BinaryFile models, run the check_vulnerable function in order on each"""
    results = [bfile.check_vulnerable() for bfile in binary_files]
    return results


@shared_task
def evaluate_vuln_by_id_range(start_id, stop_id):
    """Given a range of BinaryFile PK values, retrieve and run the check_vulnerable function in order on each
    This is function has a lower communication overhead than evalutate_vuln_by_model but has to retreive the same data before processing in each thread.
    For this reason I believe this will be the slower of the two although testing with sqlite is probably not fair
    """
    from data.models import BinaryFile
    binary_files = BinaryFile.objects.filter(pk__gte=start_id, pk__lte=stop_id)
    results = [bfile.check_vulnerable() for bfile in binary_files]
    return results
