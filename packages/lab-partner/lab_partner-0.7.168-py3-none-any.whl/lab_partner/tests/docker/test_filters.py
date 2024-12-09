from lab_partner.docker import (
    DockerContainerStatus, 
    FilterOperator, 
    FilterSet, 
    LabelFilter, 
    StatusFilter
)


def test_status_filter():
    filter = StatusFilter(DockerContainerStatus.RUNNING)
    assert str(filter) == 'status=running'


def test_status_filter_not():
    filter = StatusFilter(DockerContainerStatus.RUNNING, FilterOperator.NOT_EQUAL)
    assert str(filter) == 'status!=running'


def test_label_filter():
    filter = LabelFilter('name')
    assert str(filter) == 'label=name'


def test_label_filter_not():
    filter = LabelFilter('name', key_operator=FilterOperator.NOT_EQUAL)
    assert str(filter) == 'label!=name'


def test_label_filter_with_value():
    filter = LabelFilter('name', 'bob')
    assert str(filter) == 'label=name=bob'


def test_label_filter_not_with_value():
    filter = LabelFilter('name', 'bob', key_operator=FilterOperator.NOT_EQUAL, value_operator=FilterOperator.NOT_EQUAL)
    assert str(filter) == 'label!=name!=bob'


def test_filterset():
    status_filter = StatusFilter(DockerContainerStatus.RUNNING)
    label_filter = LabelFilter('name')
    all_filters = FilterSet() \
        .add_filter(status_filter) \
        .add_filter(label_filter) \
        .add_filter(label_filter)
    assert str(all_filters) == '-f label=name -f status=running'