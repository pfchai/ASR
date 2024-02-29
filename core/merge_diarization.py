# -*- coding: utf-8 -*-

from pyannote.core import Segment, Annotation, Timeline


PUNC_SENT_END = ['.', '?', '!', '。', '?', '！']


def get_text_with_timestamps(transcription_result):
    timestamped_texts = [(Segment(item['start'], item['end']), item['text']) for item in transcription_result['segments']]
    return timestamped_texts


def add_speaker_information(timestamped_texts, annotation):
    speaker_tagged_texts = []
    for segment, text in timestamped_texts:
        speaker = annotation.crop(segment).argmax()
        speaker_tagged_texts.append((segment, speaker, text))
    return speaker_tagged_texts


def merge_diarization_results(speaker_tagged_texts):
    merged_results = []
    sentence_buffer = []
    previous_speaker = None

    for segment, speaker, text in speaker_tagged_texts:
        if speaker != previous_speaker and previous_speaker is not None and sentence_buffer:
            merged_results.append(merge_sentences(sentence_buffer))
            sentence_buffer = [(segment, speaker, text)]
            previous_speaker = speaker
        elif text and text[-1] in PUNC_SENT_END:
            sentence_buffer.append((segment, speaker, text))
            merged_results.append(merge_sentences(sentence_buffer))
            sentence_buffer = []
            previous_speaker = speaker
        else:
            sentence_buffer.append((segment, speaker, text))
            previous_speaker = speaker

    if sentence_buffer:
        merged_results.append(merge_sentences(sentence_buffer))

    return merged_results


def diarize_text(transcription_result, diarization_result):
    timestamp_texts = get_text_with_timestamps(transcription_result)
    spk_text = add_speaker_information(timestamp_texts, diarization_result)
    res_processed = merge_diarization_results(spk_text)
    return res_processed


def merge_sentences(sentence_buffer):
    text_combined = ''.join([text for _, _, text in sentence_buffer])
    speaker = sentence_buffer[0][1]
    start = sentence_buffer[0][0].start
    end = sentence_buffer[-1][0].end
    return Segment(start, end), speaker, text_combined