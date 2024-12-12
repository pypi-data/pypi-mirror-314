import click
from .clm import clm

# from .seq2seq import seq2seq
# from .sent_transformers import sent_transformers
# from .token_classification import token_classification
# from .text_classification import text_classification


@click.group(name="finetune")
def finetune():
    """
    ScaleGen commands for managing fine-tuning deployments
    """
    pass


finetune.add_command(clm, name="clm")
# finetune.add_command(seq2seq, name="seq2seq")
# finetune.add_command(sent_transformers, name="sent_transformers")
# finetune.add_command(token_classification, name="token_classification")
# finetune.add_command(text_classification, name="text_classification")
